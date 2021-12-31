# 离线部署文档

- `OpenStack` 社区从 `Wallaby` 版本开始不再支持内部通过 `kolla-ansible 部署 Ceph 集群`。如果需要 `Ceph 集群`，则需要其它工具部署
  `Ceph`，本文档部署流程参考 <https://docs.ceph.com/en/nautilus/start/> 【使用 `ceph-deploy` 部署 `Octopus` 版本的
  ceph】
- 本文档参考了 [kolla-ansible-wallaby.md](./kolla-ansible-wallaby.md) 文档
- 操作系统使用的是 `Ubuntu 20.04`
- 全文是在 root 用户下操作，如果是其它用户，请根据实际情况进行相应的修改

## 获取离线包

离线包位于：<http://172.16.150.96/ftp/project-support/gfkd/20211220/gfkd.tar.gz>

将 gfkd.tar.gz 包上传至服务器 `/opt` 目录下并解压开 `tar -zxvf gfkd.tar.gz`。

### `pip` 离线配置

```console
# 进入目录 gfkd
root@allinone:/opt# cd /opt/gfkd

# 移动 pip.conf
root@allinone:/opt/gfkd# mkdir -p /root/.pip
root@allinone:/opt/gfkd# mv pip.conf /root/.pip/pip.conf

# 移动 pip 源文件夹
root@allinone:/opt/gfkd# mv pip /opt
```

### `apt` 离线配置

```console
# 移动 sources.list
root@allinone:/opt/gfkd# cp /etc/apt/sources.list /etc/apt/sources.list.bak
root@allinone:/opt/gfkd# mv sources.list /etc/apt/sources.list

# 解压 archives.tar.gz
root@allinone:/opt/gfkd# mv archives /opt
root@allinone:/opt/gfkd# apt-get update
```

## 部署 `OpenStack`

### 注意事项

- 本文部署是基于 `all-in-one` 的方式
- 本文安装 `kolla` 和 `kolla-ansible` 是基于 `python` 虚拟环境的方式，还有一种是直接安装在本机
- 官方文档地址 <https://docs.openstack.org/kolla-ansible/latest/user/quickstart.html>
- **各节点已经在 `/etc/hosts` 中配置了 IP 地址与主机名的对应关系**

### `Ceph` 集群操作

#### 部署 `Ceph` 集群

参考 <https://docs.ceph.com/en/nautilus/start/> 部署 Octopus 版本 Ceph。

- 安装 ceph-deploy

```console
root@allinone:/opt/gfkd# cd /opt
root@allinone:/opt# sudo apt install ceph-deploy
```

**注意：安装好 ceph-deploy 后，修改 `/usr/lib/python3/dist-packages/ceph_deploy/hosts/remotes.py` 文件，第 16、17
行。**

```python
#linux_distribution = _linux_distribution or platform.linux_distribution
distro, release, codename = ('Ubuntu', '20.04', 'focal')
```

- 创建部署文件夹

```console
root@allinone:/opt# mkdir my-cluster
root@allinone:/opt# cd my-cluster
```

- 新建集群（提供 ceph-mon 节点主机名）

```console
root@allinone:/opt/my-cluster# ceph-deploy new allinone
```

- 配置网络，在 `ceph.conf` 文件中，新增如下内容

```conf
public_network = 10.0.0.0/24
```

- 如果是单节点，需配置如下信息

```conf
osd_pool_default_size = 1
osd_pool_default_min_size = 1
```

- 安装 ceph 包

```console
root@allinone:/opt/my-cluster# ceph-deploy install --no-adjust-repos allinone
```

- ceph-mon 初始化及获取 keys

```console
root@allinone:/opt/my-cluster# ceph-deploy mon create-initial
```

- 拷贝 ceph 配置文件至 `/etc/ceph` 目录下

```console
root@allinone:/opt/my-cluster# ceph-deploy admin allinone
```

- 部署 ceph-mgr 服务

```conosle
root@allinone:/opt/my-cluster# ceph-deploy mgr create allinone
```

- 添加 ceph-osd 服务

```console
root@allinone:/opt/my-cluster# ceph-deploy osd create --data /dev/sdb allinone
root@allinone:/opt/my-cluster# ceph-deploy osd create --data /dev/sdc allinone
```

- 添加 ceph-rgw 服务

```console
root@allinone:/opt/my-cluster# ceph-deploy rgw create allinone
```

修改 ceph.conf 配置文件，增加如下内容

```conf
[client.rgw.allinone]
host=allinone
log file=/var/log/radosgw/client.radosgw.gateway.log
rgw_frontends = civetweb port=8081
```

重启 ceph-rgw

```console
root@allinone:/opt/my-cluster# ceph-deploy --overwrite-conf admin allinone
root@allinone:/opt/my-cluster# systemctl restart ceph-radosgw@rgw.allinone.service
```

#### 验证 `ceph` 集群

```console
root@allinone:/opt/my-cluster# ceph -s
  cluster:
    id:     d01386e6-56c5-4418-ae1b-383168deece7
    health: HEALTH_WARN
            mon is allowing insecure global_id reclaim
            1 pool(s) have no replicas configured

  services:
    mon: 1 daemons, quorum allinone (age 3m)
    mgr: allinone(active, since 88s)
    osd: 2 osds: 2 up (since 16s), 2 in (since 16s)

  task status:

  data:
    pools:   1 pools, 1 pgs
    objects: 0 objects, 0 B
    usage:   2.0 GiB used, 98 GiB / 100 GiB avail
    pgs:     1 active+clean
```

#### 创建池和 auth

```console
root@allinone:/opt/my-cluster# ceph osd pool create volumes 64 64
root@allinone:/opt/my-cluster# ceph osd pool create backups 64 64
root@allinone:/opt/my-cluster# ceph osd pool create vms 64 64
root@allinone:/opt/my-cluster# ceph osd pool create images 64 64
root@allinone:/opt/my-cluster# ceph auth get-or-create client.cinder mon 'profile rbd' osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd pool=images'
root@allinone:/opt/my-cluster# ceph auth get-or-create client.cinder-backup mon 'profile rbd' osd 'profile rbd pool=backups'
root@allinone:/opt/my-cluster# ceph auth get-or-create client.glance mon 'profile rbd' osd 'profile rbd pool=images'
root@allinone:/opt/my-cluster# ceph auth get-or-create client.nova mon 'profile rbd' osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd pool=images'
root@allinone:/opt/my-cluster# ceph osd pool ls detail
pool 1 'device_health_metrics' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 1 pgp_num 1 autoscale_mode on last_change 9 flags hashpspool stripe_width 0 pg_num_min 1 application mgr_devicehealth
pool 2 'volumes' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 64 pgp_num 64 autoscale_mode on last_change 18 flags hashpspool stripe_width 0
pool 3 'backups' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 64 pgp_num 64 autoscale_mode on last_change 21 flags hashpspool stripe_width 0
pool 4 'vms' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 64 pgp_num 64 autoscale_mode on last_change 24 flags hashpspool stripe_width 0
pool 5 'images' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 64 pgp_num 64 autoscale_mode on last_change 27 flags hashpspool stripe_width 0
root@allinone:/opt/my-cluster# ceph auth list
......
client.cinder
        key: AQB49YthKZ/lABAAHBdWtjivBI/T4VyfEM2TxQ==
        caps: [mon] profile rbd
        caps: [osd] profile rbd pool=volumes, profile rbd pool=vms, profile rbd pool=images
client.cinder-backup
        key: AQBs9YthJ6HsARAAUB7VIOxm/gcpzz2JF9biJw==
        caps: [mon] profile rbd
        caps: [osd] profile rbd pool=backups
client.glance
        key: AQBi9YthQxNbKBAAT7LZw0AJDM8NR4nSvaThHw==
        caps: [mon] profile rbd
        caps: [osd] profile rbd pool=images
client.nova
        key: AQBY9YtheX/SKxAA81Aqd6RCcNXmiEVo3Xco1w==
        caps: [mon] profile rbd
        caps: [osd] profile rbd pool=volumes, profile rbd pool=vms, profile rbd pool=images
......
```

### `openstack` 集群操作

#### 安装依赖并创建虚拟环境

```console
root@allinone:/opt/my-cluster# cd ~
# 安装依赖
root@allinone:~# sudo apt install -y python3-dev libffi-dev gcc libssl-dev
# 安装python虚拟环境
root@allinone:~# sudo apt install -y python3-venv
# 创建虚拟环境
root@allinone:~# python3 -m venv .venv
# 进入虚拟环境
root@allinone:~# source .venv/bin/activate
# 更新或安装最新版本的pip
(.venv) root@allinone:~# pip install -U pip
# 安装 ansible
(.venv) root@allinone:~# pip install 'ansible<3.0'
```

### 安装 `kolla-ansible`

1. 安装 kolla-ansible

```console
# 进入虚拟环境
root@allinone:~# source .venv/bin/activate
(.venv) root@allinone:~# pip install kolla-ansible
(.venv) root@allinone:~# deactivate
```

2. 创建 `/etc/kolla` 目录，并修改目录权限

```console
root@allinone:~# sudo mkdir -p /etc/kolla
root@allinone:~# sudo chown $USER:$USER /etc/kolla
```

3. 把 `globals.yml` 和 `password.yml` 复制到 `/etc/kolla` 文件夹下

```console
root@allinone:~# cp .venv/share/kolla-ansible/etc_examples/kolla/* /etc/kolla
```

4. 将单节点和多节点的配置文件复制到该目录下

```console
root@allinone:~# cp .venv/share/kolla-ansible/ansible/inventory/* .
```

5. 配置 `ansible`

```console
root@allinone:~# mkdir /etc/ansible
root@allinone:~# cat << EOF > /etc/ansible/ansible.cfg
[defaults]
host_key_checking=False
pipelining=True
forks=100
EOF
```

### 初始化配置

1. `all-in-one` 配置见如下，下述为文件前半部分

```ini
# These initial groups are the only groups required to be modified. The
# additional groups are for more control of the environment.
[control]
10.0.0.141 ansible_user=root ansible_password=99cloud ansible_become=true

[network]
10.0.0.141 ansible_user=root ansible_password=99cloud ansible_become=true

[compute]
10.0.0.141 ansible_user=root ansible_password=99cloud ansible_become=true

[storage]
10.0.0.141 ansible_user=root ansible_password=99cloud ansible_become=true

[monitoring]
10.0.0.141 ansible_user=root ansible_password=99cloud ansible_become=true

[deployment]
localhost       ansible_connection=local
......
```

2. 检查配置

```console
root@allinone:~# sudo apt-get install -y sshpass
root@allinone:~# source .venv/bin/activate
(.venv) root@allinone:~# ansible -i all-in-one all -m ping
```

3. 初始化密码

```console
(.venv) root@allinone:~# kolla-genpwd
(.venv) root@allinone:~# deactivate
```

4. `globals.yml` 配置见如下，下述为文件中打开的选项：

```yaml
---
kolla_base_distro: "ubuntu"
kolla_install_type: "source"
openstack_release: "wallaby"
kolla_internal_vip_address: "10.0.0.251"
kolla_external_vip_address: "10.0.0.252"
docker_registry: 10.0.0.141:4000
docker_namespace: "kolla"
network_interface: "ens3"
neutron_external_interface: "ens4"
openstack_logging_debug: "True"
enable_openstack_core: "yes"
enable_glance: "{{ enable_openstack_core | bool }}"
enable_haproxy: "yes"
enable_keepalived: "{{ enable_haproxy | bool }}"
enable_keystone: "{{ enable_openstack_core | bool }}"
enable_mariadb: "yes"
enable_memcached: "yes"
enable_neutron: "{{ enable_openstack_core | bool }}"
enable_nova: "{{ enable_openstack_core | bool }}"
enable_rabbitmq: "{{ 'yes' if om_rpc_transport == 'rabbit' or om_notify_transport == 'rabbit' else 'no' }}"
enable_cinder: "yes"
enable_cinder_backup: "yes"
enable_fluentd: "yes"
enable_horizon: "{{ enable_openstack_core | bool }}"
enable_ironic: "yes"
enable_ironic_ipxe: "yes"
enable_ironic_neutron_agent: "{{ enable_neutron | bool and enable_ironic | bool }}"
enable_ironic_pxe_uefi: "yes"
enable_neutron_vpnaas: "yes"
enable_neutron_qos: "yes"
enable_octavia: "yes"
enable_prometheus: "yes"
glance_backend_ceph: "yes"
ceph_glance_keyring: ceph.client.glance.keyring
ceph_glance_user: glance
ceph_glance_pool_name: images
glance_backend_file: "no"
cinder_backend_ceph: "yes"
ceph_cinder_keyring: ceph.client.cinder.keyring
ceph_cinder_user: cinder
ceph_cinder_pool_name: volumes
ceph_cinder_backup_keyring: ceph.client.cinder-backup.keyring
ceph_cinder_backup_user: cinder-backup
ceph_cinder_backup_pool_name: backups
nova_backend_ceph: "yes"
ceph_nova_keyring: ceph.client.nova.keyring
ceph_nova_user: nova
ceph_nova_pool_name: vms
ironic_dnsmasq_interface: "{{ network_interface }}"
ironic_dnsmasq_dhcp_range: "10.0.0.10,10.0.0.50,255.255.255.0"
ironic_cleaning_network: "public1"
octavia_auto_configure: "yes"
octavia_amp_image_tag: "amphora"
octavia_loadbalancer_topology: "SINGLE"
enable_docker_repo: false
prechecks_enable_host_ntp_checks: false
```

5. 获取 `ironic kernel` 以及 `initramfs` 镜像。并且配置 `ceph` 的信息。

```console
# ironic kernel and initramfs
root@allinone:~# mkdir -p /etc/kolla/config/ironic
root@allinone:~# cp /opt/gfkd/ironic-agent.kernel /etc/kolla/config/ironic/
root@allinone:~# cp /opt/gfkd/ironic-agent.initramfs /etc/kolla/config/ironic/
# 配置 glance 的 ceph 信息
root@allinone:~# mkdir -p /etc/kolla/config/glance
root@allinone:~# ssh root@10.0.0.141 sudo tee /etc/kolla/config/glance/ceph.conf </etc/ceph/ceph.conf
root@allinone:~# ceph auth get-or-create client.glance | ssh root@10.0.0.141 sudo tee /etc/kolla/config/glance/ceph.client.glance.keyring
# 配置 nova 的 ceph 信息
root@allinone:~# mkdir -p /etc/kolla/config/nova
root@allinone:~# ssh root@10.0.0.141 sudo tee /etc/kolla/config/nova/ceph.conf </etc/ceph/ceph.conf
root@allinone:~# ceph auth get-or-create client.cinder | ssh root@10.0.0.141 sudo tee /etc/kolla/config/nova/ceph.client.cinder.keyring
root@allinone:~# ceph auth get-or-create client.nova | ssh root@10.0.0.141 sudo tee /etc/kolla/config/nova/ceph.client.nova.keyring
# 配置 cinder 的 ceph 信息
root@allinone:~# mkdir -p /etc/kolla/config/cinder
root@allinone:~# ssh root@10.0.0.141 sudo tee /etc/kolla/config/cinder/ceph.conf </etc/ceph/ceph.conf
root@allinone:~# mkdir -p /etc/kolla/config/cinder/cinder-volume
root@allinone:~# ceph auth get-or-create client.cinder | ssh root@10.0.0.141 sudo tee /etc/kolla/config/cinder/cinder-volume/ceph.client.cinder.keyring
root@allinone:~# mkdir -p /etc/kolla/config/cinder/cinder-backup
root@allinone:~# ceph auth get-or-create client.cinder | ssh root@10.0.0.141 sudo tee /etc/kolla/config/cinder/cinder-backup/ceph.client.cinder.keyring
root@allinone:~# ceph auth get-or-create client.cinder-backup | ssh root@10.0.0.141 sudo tee /etc/kolla/config/cinder/cinder-backup/ceph.client.cinder-backup.keyring
```

### 部署

- `openstack` 部署

```console
root@allinone:~# source .venv/bin/activate
(.venv) root@allinone:~# kolla-ansible octavia-certificates
(.venv) root@allinone:~# kolla-ansible -i all-in-one bootstrap-servers
(.venv) root@allinone:~# kolla-ansible -i all-in-one prechecks
(.venv) root@allinone:~# deactivate
```

- 启用 `registry`

```console
root@allinone:~# cd /opt/gfkd/
root@allinone:/opt/gfkd# cd images/
root@allinone:/opt/gfkd/images# docker load -i registry.tar
root@allinone:/opt/gfkd/images# docker run -d --net=host --restart=always -v /opt/gfkd/config.yml:/etc/docker/registry/config.yml --name registry registry:2
```

- 修改 `/etc/docker/daemon.json` 文件，新增如下信息

```json
"insecure-registries": ["10.0.0.141:4000"]
```

- 重启 docker

```console
root@allinone:/opt/gfkd/images# systemctl restart docker
```

- 导入所有镜像，并且上传至 registry 中

```console
root@allinone:/opt/gfkd/images# for i in `ll | grep tar | awk '{print $9}'`;do docker load -i $i;done
root@allinone:/opt/gfkd/images# for i in `docker images | grep wallaby | awk '{print $1}'`;do docker tag $i:wallaby 10.0.0.141:4000/$i:wallaby;docker rmi $i:wallaby;docker push 10.0.0.141:4000/$i:wallaby;done
```

- 开始部署

```console
root@allinone:/opt/gfkd/images# cd ~
root@allinone:~# source .venv/bin/activate
(.venv) root@allinone:~# kolla-ansible -i all-in-one deploy
(.venv) root@allinone:~# kolla-ansible post-deploy
(.venv) root@allinone:~# deactivate
```

- 安装 `opesntack` 客户端

```console
# 安装客户端
root@allinone:~# pip install python-openstackclient
# 把admin用户信息添加到环境变量中
root@allinone:~# . /etc/kolla/admin-openrc.sh
root@allinone:~# mkdir -p /opt/cache/files/
root@allinone:~# cp /opt/gfkd/cirros-0.5.1-x86_64-disk.img /opt/cache/files/
# 创建示范网络和下载所需要的测试镜像
root@allinone:~# /root/.venv/share/kolla-ansible/init-runonce
```

- 上传 octavia amphora 镜像

```console
root@allinone:~# cd /opt/gfkd
root@allinone:/opt/gfkd# source /etc/kolla/octavia-openrc.sh
root@allinone:/opt/gfkd# openstack image create amphora-x64-haproxy.qcow2 --container-format bare --disk-format qcow2 --private --tag amphora --file amphora-x64-haproxy.qcow2 --property hw_architecture='x86_64' --property hw_rng_model=virtio
```

- 修改 `octavia` 使用的 `net`

```console
root@allinone:~# source /etc/kolla/admin-openrc.sh
root@allinone:~# neutron router-gateway-clear 77d3f9ec-c78c-450f-a8df-8d5dabea228a
root@allinone:~# openstack router delete demo-router
root@allinone:~# openstack network delete public1
root@allinone:~# OCTAVIA_MGMT_SUBNET=10.10.0.0/24
root@allinone:~# OCTAVIA_MGMT_SUBNET_START=10.10.0.210
root@allinone:~# OCTAVIA_MGMT_SUBNET_END=10.10.0.220
root@allinone:~# source /etc/kolla/octavia-openrc.sh
root@allinone:~# openstack network create public1 --provider-network-type flat --provider-physical-network physnet1 --external --share
root@allinone:~# openstack subnet create --subnet-range $OCTAVIA_MGMT_SUBNET --allocation-pool start=$OCTAVIA_MGMT_SUBNET_START,end=$OCTAVIA_MGMT_SUBNET_END --network public1 subnet
root@allinone:~# NET_NETWORK_ID=`openstack network show public1 -f value -c id`
root@allinone:~# sed -i "s/^amp_boot_network_list = *.*/amp_boot_network_list = $NET_NETWORK_ID/g" /etc/kolla/octavia-api/octavia.conf
root@allinone:~# sed -i "s/^amp_boot_network_list = *.*/amp_boot_network_list = $NET_NETWORK_ID/g" /etc/kolla/octavia-health-manager/octavia.conf
root@allinone:~# sed -i "s/^amp_boot_network_list = *.*/amp_boot_network_list = $NET_NETWORK_ID/g" /etc/kolla/octavia-housekeeping/octavia.conf
root@allinone:~# sed -i "s/^amp_boot_network_list = *.*/amp_boot_network_list = $NET_NETWORK_ID/g" /etc/kolla/octavia-worker/octavia.conf
root@allinone:~# docker restart octavia_api octavia_health_manager octavia_housekeeping octavia_worker
```

- 上传 `ironic kernel` 和 `initramfs` 镜像

```console
root@allinone:~# source /etc/kolla/admin-openrc.sh
root@allinone:~# openstack image create --disk-format ari --container-format ari --public --file /etc/kolla/config/ironic/ironic-agent.initramfs deploy-initrd
root@allinone:~# openstack image create --disk-format aki --container-format aki --public --file /etc/kolla/config/ironic/ironic-agent.kernel deploy-vmlinuz
```

## 配置 `swift`

- 修改 ceph.conf 配置文件

```conf
[client.rgw.allinone]
host=allinone
log file=/var/log/client.radosgw.gateway.log
rgw_frontends = civetweb port=8081
rgw keystone api version = 3
rgw keystone url = 10.0.0.251:5000
rgw keystone accepted roles = admin,reader,_member_,member
rgw keystone token cache size = 500
rgw keystone revocation interval = 300
rgw keystone implicit tenants = true
rgw s3 auth use keystone = true
rgw keystone admin user = admin
rgw keystone admin password = 5caVKZ7MGTwGR2Le1jCtAz0mwvlnHdgvDXlT3Q9C
rgw keystone admin tenant = admin
rgw keystone admin domain = Default
rgw swift account in url = true
rgw bucket quota ttl = 0
rgw user quota bucket sync interval = 0
rgw user quota sync interval = 0
```

```console
root@allinone:~# cd /opt/my-cluster
root@allinone:/opt/my-cluster# ceph-deploy --overwrite-conf admin allinone
root@allinone:/opt/my-cluster# systemctl restart ceph-radosgw@rgw.allinone.service
```

- 创建 endpoint

```console
root@allinone:/opt/my-cluster# source /etc/kolla/admin-openrc.sh
root@allinone:/opt/my-cluster# openstack service create --name swift --description "OpenStack Object Storage" object-store
root@allinone:/opt/my-cluster# openstack endpoint create --region RegionOne object-store public "http://10.0.0.252:8081/swift/v1/AUTH_%(tenant_id)s"
root@allinone:/opt/my-cluster# openstack endpoint create --region RegionOne object-store internal "http://10.0.0.251:8081/swift/v1/AUTH_%(tenant_id)s"
root@allinone:/opt/my-cluster# openstack endpoint create --region RegionOne object-store admin "http://10.0.0.251:8081/swift/v1/AUTH_%(tenant_id)s"
```

### 部署 `skyline`

直接使用提供的 `skyline` 镜像，详细的部署流程参考数据库使用 `mariaDB` 部署，文档地址为
<https://opendev.org/skyline/skyline-apiserver/src/branch/master/README-zh_CN.md>

启动容器后根据实际环境修改 `/etc/skyline/skyline.yaml` ，修改完毕查看 `skyline` 容器日志判断服务是否正常运行，如果出现 401 权限校验问题查看
`system_user_password` 是否正确，出现 `url` 问题把 `localhost` 改为本机的 `ip` 地址，出现数据库问题查看 `database_url` 是否配置正确

### 添加企业的 `openstack-exporter`

添加云主机 `top 5` 的 `metric`, 把企业的 `openstack-exporter` 镜像添加到装有社区版的环境中

#### 修改企业 `openstack-exporter` 的配置文件

1. 创建 `openstack-exporter` 配置文件目录

```console
root@allinone:~# mkdir -p /etc/openstack-exporter
```

2. 添加配置文件

```console
# /etc/openstack-exporter/uwsgi.ini
root@allinone:~# cat <<EOF> /etc/openstack-exporter/uwsgi.ini
[uwsgi]
http = 10.0.0.252:9183
module = openstack_exporter.main:app
callable = app
processes = 1
threads = 10
stats = 10.0.0.252:9185
EOF

# /etc/openstack-exporter/openstack_exporter.conf
root@allinone:~# cat <<EOF> /etc/openstack-exporter/openstack_exporter.conf
[DEFAULT]
address = "10.0.0.252"
port = "9183"

[keystone_authtoken]
auth_type = "password"
auth_url = "http://10.0.0.252:5000/v3"
project_name = "admin"
project_domain_name = "Default"
username = "admin"
user_domain_name = "Default"
password = "damnPJhPVkEs3gNmM0lKuupptTkyQFq199NgfJYj"

[exporter]
default_interval = 240
enable_sync_metrics = instance.info,os.hostaggregate_common,os.hostaggregate_host,os.hypervisor_common,os.hypervisor_ovs,os.hypervisor_sriov,os.services,instance.cpu,instance.disk,instance.interface,instance.mem,instance.watchdog_event,node.chrony_server_synchronized,node.info,node.ict_process_total,node.dns_status
enable_async_metrics =

[process]
required_processes = nova-novncproxy,libvirtd,nova-compute,neutron-openvswitch-agent,nova-conductor,nova-api,cinder-api,cinder-volume,neutron-l3-agent,neutron-metadata-agent,neutron-dhcp-agent,nova-scheduler,neutron-server,glance-api,heat-engine,heat-api,cinder-scheduler
EOF
```

3. 添加 `prometheus-server` 的 `rules` 用于部分指标计算

```console
root@allinone:~# cat <<EOF> /etc/kolla/prometheus-server/openstack_exporter.rules
---
groups:
  - name: openstack exporter recording
    rules:
      # cpu
      - record: virtual:kvm:cpu:count
        expr: os_instance_cpu_vcpus
      - record: virtual:kvm:cpu:usage
        expr: clamp_min(clamp_max(irate(os_instance_cpu_cpu_time[5m])/os_instance_cpu_vcpus/1e+9, 1), 0)
      # memory
      - record: virtual:kvm:memory:total
        expr: os_instance_memory_actual
      - record: virtual:kvm:memory:used
        expr: os_instance_memory_used
      # network
      - record: virtual:kvm:network:receive:rate
        expr: irate(os_instance_interface_net_read_bytes[5m])
      - record: virtual:kvm:network:write:rate
        expr: irate(os_instance_interface_net_write_bytes[5m])
      - record: virtual:kvm:network:transmit:rate
        expr: irate(os_instance_interface_net_write_bytes[5m])
      # disk
      - record: virtual:kvm:disk:read:kbps
        expr: irate(os_instance_disk_read_bytes[5m])
      - record: virtual:kvm:disk:write:kbps
        expr: irate(os_instance_disk_write_bytes[5m])
      - record: virtual:kvm:disk:read:iops
        expr: irate(os_instance_disk_read_requests_issued[5m])
      - record: virtual:kvm:disk:write:iops
        expr: irate(os_instance_disk_write_requests_issued[5m])
```

4. 在 `/etc/kolla/prometheus-server/prometheus.yml` 配置文件中增加配置

```yaml
rule_files:
  - /etc/prometheus/openstack_exporter.rules
```

5. 启动 `openstack-exporter` 服务

```console
root@allinone:~# docker run -d --name openstack_exporter --pid=host --privileged --restart=always -v /etc/openstack-exporter:/etc/openstack-exporter -v /etc/localtime:/etc/localtime -v /run/libvirt:/run/libvirt -v /etc/pki:/etc/pki -v /run/netns:/run/netns -v /run/openvswitch:/run/openvswitch --net=host openstack-exporter/openstack-exporter:latest uwsgi --ini /etc/openstack-exporter/uwsgi.ini
```

6. cinder.conf 配置文件中， `[rbd-1]` 配置项下新增配置

```console
rbd_exclusive_cinder_pool = False
```

7. 重启容器

```console
root@allinone:~# docker restart prometheus_server cinder_volume openstack_exporter
```

### 社区的 `openstack-exporter` 添加 `cinder metric`

默认 `openstack-exporter cinder metric` 使用的是 `v2` 版本的 `api` ，在没有 `v2` 版本时要修改配置文件
`/etc/kolla/prometheus-openstack-exporter/clouds.yml` 在文件中添加`volume_api_version: v3`，添加示例如下。添加后重启
`openstack-exporter` 容器即可，重启命令为 `docker restart prometheus_openstack_exporter`

```yaml
clouds:
 default:
   region_name: RegionOne
   volume_api_version: v3
   identity_api_version: 3
   identity_interface: internal
   auth:
     username: admin
     password: VC7J5ZUD2WLSqmL2VxR0wErUWLhRvEB9ZSkq7FC5
     project_name: admin
     project_domain_name: 'Default'
     user_domain_name: 'Default'
     cacert:
     auth_url: http://192.168.100.60:35357/v3
```

### 修改 `stack` 的访问权限

- 进入 heat-api 容器，生成 polic.yaml 文件

```console
root@allinone:~# docker exec -it -uroot heat_api bash
(heat-api)[root@allinone /]# oslopolicy-sample-generator --config-file etc/heat/heat-policy-generator.conf
(heat-api)[root@allinone /]# exit
root@allinone:~# docker cp heat_api:/etc/heat/policy.yaml.sample /etc/kolla/heat-api/policy.yaml
```

- 修改 `heat` 服务中 `/v1/{tenant_id}/stacks` 接口的访问权限，修改后如下

```yaml
# List stacks globally.
# GET  /v1/{tenant_id}/stacks
# Intended scope(s): system, project
# "stacks:global_index": "role:reader and system_scope:all"
"stacks:global_index": "role:admin"
```

- 修改 config.json 文件，新增如下信息

```yaml
,
        {
            "source": "/var/lib/kolla/config_files/policy.yaml",
            "dest": "/etc/heat/policy.yaml",
            "owner": "heat",
            "perm": "0600"
        }
```

- 修改 heat.conf 配置文件，新增如下信息

```conf
[oslo_policy]
policy_file = policy.yaml
```

- 重启 `heat` 服务

```console
root@allinone:~# docker restart heat-api
```

## 更新 prometheus 配置

打开 ceph export（在 ceph mgr 节点）

```bash
ceph mgr module enable prometheus --force

# 查看端口，确认 ceph exporter 正常
ss -an | grep 9283
```

刚推完成后的 prometheus 不包含 ceph 和企业版额外的 openstack exporter，需要修改配置文件（在尾部增加如下行），予以纳管

```console
(.venv) root@control01:~# cat /etc/kolla/prometheus-server/prometheus.yml 
alerting:
  ...
global:
  ...
scrape_configs:
- ...
- job_name: ceph
  static_configs:
  - targets:
    - 172.16.11.1:9283
- job_name: openstack_exporter_plus
  static_configs:
  - targets:
    - 172.16.11.1:9183
    - 172.16.11.2:9183
    - 172.16.11.3:9183
    - 172.16.11.4:9183
    - 172.16.11.5:9183
rule_files:
  - /etc/prometheus/openstack_exporter.rules
```

然后把文件推送到所有控制节点（计算节点没有安装 prometheus server）

``` bash
cd ~
. .venv/bin/activate

ansible -i multinode control -m copy -a 'src=/etc/kolla/prometheus-server/prometheus.yml dest=/etc/kolla/prometheus-server/prometheus.yml'
```

重启控制节点的 prometheus server

```bash
ansible -i multinode control -m shell -a 'docker restart prometheus_server'
```

然后在 prometheus dashboard 上 <http://172.16.11.250:9091/targets> 就可以看到新添加的 ceph 和 `openstack_exporter_plus` 的内容


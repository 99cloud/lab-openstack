# 更多插件的部署文档

- `openstack` 社区 w 版已经不在支持内部的 `ceph` ，如果需要则要单独部署 `ceph` ，部署流程参考
  <https://docs.ceph.com/en/nautilus/start/>
- 本文档基于 [kolla-ansible-wallaby.md](kolla-ansible-wallaby.md) 文档编写
- 操作系统使用的是 `Ubuntu20.04`

## 开启 `swift`

在部署 `openstack` 之前进行对 `swift` 的初始化操作

1. 初始化数据盘作为 `swift` 的存储设备，获取数据盘信息使用 `fdisk -l`

```
index=0
for d in <disk_label>; do
    free_device=$(losetup -f)
    fallocate -l 1G /tmp/$d
    losetup $free_device /tmp/$d
    parted $free_device -s -- mklabel gpt mkpart KOLLA_SWIFT_DATA 1 -1
    sudo mkfs.xfs -f -L d${index} ${free_device}p1
    (( index++ ))
done
```

2. 添加 `swift` 环境变量

```
STORAGE_NODES=(192.168.100.133)
KOLLA_SWIFT_BASE_IMAGE="kolla/ubuntu-source-swift-base:4.0.0"
mkdir -p /etc/kolla/config/swift
```

3. 生成 `swift` 所需要的 `ring`

```
docker run \
  --rm \
  -v /etc/kolla/config/swift/:/etc/kolla/config/swift/ \
  $KOLLA_SWIFT_BASE_IMAGE \
  swift-ring-builder \
    /etc/kolla/config/swift/object.builder create 10 3 1

for node in ${STORAGE_NODES[@]}; do
    for i in {0..2}; do
      docker run \
        --rm \
        -v /etc/kolla/config/swift/:/etc/kolla/config/swift/ \
        $KOLLA_SWIFT_BASE_IMAGE \
        swift-ring-builder \
          /etc/kolla/config/swift/object.builder add r1z1-${node}:6000/d${i} 1;
    done
done
```

```
docker run \
  --rm \
  -v /etc/kolla/config/swift/:/etc/kolla/config/swift/ \
  $KOLLA_SWIFT_BASE_IMAGE \
  swift-ring-builder \
    /etc/kolla/config/swift/account.builder create 10 3 1

for node in ${STORAGE_NODES[@]}; do
    for i in {0..2}; do
      docker run \
        --rm \
        -v /etc/kolla/config/swift/:/etc/kolla/config/swift/ \
        $KOLLA_SWIFT_BASE_IMAGE \
        swift-ring-builder \
          /etc/kolla/config/swift/account.builder add r1z1-${node}:6001/d${i} 1;
    done
done
```

```
docker run \
  --rm \
  -v /etc/kolla/config/swift/:/etc/kolla/config/swift/ \
  $KOLLA_SWIFT_BASE_IMAGE \
  swift-ring-builder \
    /etc/kolla/config/swift/container.builder create 10 3 1

for node in ${STORAGE_NODES[@]}; do
    for i in {0..2}; do
      docker run \
        --rm \
        -v /etc/kolla/config/swift/:/etc/kolla/config/swift/ \
        $KOLLA_SWIFT_BASE_IMAGE \
        swift-ring-builder \
          /etc/kolla/config/swift/container.builder add r1z1-${node}:6002/d${i} 1;
    done
done
```

```
for ring in object account container; do
  docker run \
    --rm \
    -v /etc/kolla/config/swift/:/etc/kolla/config/swift/ \
    $KOLLA_SWIFT_BASE_IMAGE \
    swift-ring-builder \
      /etc/kolla/config/swift/${ring}.builder rebalance;
done
```

## 部署 `openstack`

### 注意事项

- 本文部署是基于 `all-in-one` 的方式
- 本文安装 `kolla` 和 `kolla-ansible` 是基于 `python` 虚拟环境的方式，还有一种是直接安装在本机
- 本文部署方式是以源码形式部署，同样还有不基于源码形式部署
- 官方文档地址 <https://docs.openstack.org/kolla-ansible/latest/user/quickstart.html>

### `ceph` 集群操作

#### 验证 `ceph` 集群

```console
root@ceph-nautilus-allinone:~# ceph -s
  cluster:
    id:     61597978-90c8-4d19-b6b8-c6f8d29096a7
    health: HEALTH_WARN
            4 pool(s) have no replicas configured
            application not enabled on 3 pool(s)
            mon is allowing insecure global_id reclaim

  services:
    mon: 1 daemons, quorum ceph-nautilus-allinone (age 15h)
    mgr: ceph-nautilus-allinone(active, since 15h)
    osd: 2 osds: 2 up (since 15h), 2 in (since 15h)

  data:
    pools:   4 pools, 256 pgs
    objects: 691 objects, 2.1 GiB
    usage:   3.8 GiB used, 196 GiB / 200 GiB avail
    pgs:     256 active+clean

  io:
    client:   2.0 KiB/s wr, 0 op/s rd, 0 op/s wr
```

#### 创建池和 auth

```console
root@ceph-nautilus-allinone:~# ceph osd pool create volumes 64 64
root@ceph-nautilus-allinone:~# ceph osd pool create backups 64 64
root@ceph-nautilus-allinone:~# ceph osd pool create vms 64 64
root@ceph-nautilus-allinone:~# ceph osd pool create images 64 64
root@ceph-nautilus-allinone:~# ceph auth get-or-create client.cinder mon 'profile rbd' osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd pool=images'
root@ceph-nautilus-allinone:~# ceph auth get-or-create client.cinder-backup mon 'profile rbd' osd 'profile rbd pool=backups'
root@ceph-nautilus-allinone:~# ceph auth get-or-create client.glance mon 'profile rbd' osd 'profile rbd pool=images'
root@ceph-nautilus-allinone:~# ceph auth get-or-create client.nova mon 'profile rbd' osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd pool=images'
root@ceph-nautilus-allinone:~# ceph osd pool ls detail
pool 1 'volumes' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 64 pgp_num 64 autoscale_mode warn last_change 27 flags hashpspool,selfmanaged_snaps stripe_width 0
        removed_snaps [1~3]
pool 2 'vms' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 64 pgp_num 64 autoscale_mode warn last_change 31 flags hashpspool,selfmanaged_snaps stripe_width 0
        removed_snaps [1~3]
pool 3 'backups' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 64 pgp_num 64 autoscale_mode warn last_change 18 flags hashpspool stripe_width 0
pool 4 'images' replicated size 1 min_size 1 crush_rule 0 object_hash rjenkins pg_num 64 pgp_num 64 autoscale_mode warn last_change 34 flags hashpspool,selfmanaged_snaps stripe_width 0
        removed_snaps [1~3]
root@ceph-nautilus-allinone:~# ceph auth list
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

#### `ubuntu` 换源（可选）

```console
# 先备份以防以后需要使用
root@kolla-ansible-w:~# sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
# 添加阿里的镜像源
root@kolla-ansible-w:~# cat << EOF > /etc/apt/sources.list
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
EOF
# 更新源
sudo apt update
```

#### 安装依赖并创建虚拟环境

```console
# 安装依赖
root@kolla-ansible-w:~# sudo apt install -y python3-dev libffi-dev gcc libssl-dev
# 安装python虚拟环境
root@kolla-ansible-w:~# sudo apt install -y python3-venv
# 创建虚拟环境
root@kolla-ansible-w:~# python3 -m venv /path/to/venv
# 进入虚拟环境
root@kolla-ansible-w:~# source /path/to/venv/bin/activate
# 更新或安装最新版本的pip
root@kolla-ansible-w:~# pip install -U pip
# 安装 ansible
root@kolla-ansible-w:~# pip install -i https://pypi.douban.com/simple/ 'ansible<3.0'
```

### 安装 `kolla` 和 `kolla-ansible`

1. 下载源码

```console
root@kolla-ansible-w:~# cd /opt
root@kolla-ansible-w:~# git clone -b stable/wallaby https://github.com/openstack/kolla
root@kolla-ansible-w:~# git clone -b stable/wallaby https://github.com/openstack/kolla-ansible
```

2. 安装项目所需要的 `python` 包

```console
root@kolla-ansible-w:~# pip install -i https://pypi.douban.com/simple/ /opt/kolla
root@kolla-ansible-w:~# pip install -i https://pypi.douban.com/simple/ /opt/kolla-ansible
```

3. 创建 `/etc/kolla` 目录，并修改目录权限

```console
root@kolla-ansible-w:~# sudo mkdir -p /etc/kolla
root@kolla-ansible-w:~# sudo chown $USER:$USER /etc/kolla
```

4. 把 `globals.yml` 和 `password.yml` 复制到 `/etc/kolla` 文件夹下

```console
root@kolla-ansible-w:~# cp -r /opt/kolla-ansible/etc/kolla/* /etc/kolla
```

5. 将单节点和多节点的配置文件复制到该目录下

```console
root@kolla-ansible-w:~# cp /opt/kolla-ansible/ansible/inventory/* .
```

6. 配置 `ansible`

```console
root@kolla-ansible-w:~# mkdir /etc/ansible
root@kolla-ansible-w:~# cat << EOF > /etc/ansible/ansible.cfg
[defaults]
host_key_checking=False
pipelining=True
forks=100
ansible_python_interpreter=/path/to/venv/bin/python3
EOF
```

### 初始化配置

1. `all-in-one` 配置见如下，下述为文件前半部分

```ini
# These initial groups are the only groups required to be modified. The
# additional groups are for more control of the environment.
[control]
192.168.100.149 ansible_user=root ansible_password=99cloud ansible_become=true

[network]
192.168.100.149 ansible_user=root ansible_password=99cloud ansible_become=true

[compute]
192.168.100.149 ansible_user=root ansible_password=99cloud ansible_become=true

[storage]
192.168.100.149 ansible_user=root ansible_password=99cloud ansible_become=true

[monitoring]
192.168.100.149 ansible_user=root ansible_password=99cloud ansible_become=true

[deployment]
localhost       ansible_connection=local
......
```

2. 检查配置

```console
root@kolla-ansible-w:~# ansible -i all-in-one all -m ping
```

3. 初始化密码

```console
root@kolla-ansible-w:~# cd /opt/kolla-ansible/tools
root@kolla-ansible-w:~# ./generate_passwords.py
```

4. `globals.yml` 配置见如下，下述为文件中打开的选项：

```yaml
---
kolla_base_distro: "ubuntu"
kolla_install_type: "source"
openstack_release: "wallaby"
kolla_internal_vip_address: "192.168.100.149"
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
enable_swift: "yes"
enable_swift_s3api: "yes"
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
ironic_dnsmasq_dhcp_range: "192.168.100.210,192.168.100.220,255.255.255.0"
ironic_cleaning_network: "public1"
octavia_auto_configure: "yes"
octavia_amp_image_tag: "amphora"
octavia_loadbalancer_topology: "SINGLE"
```

5. 获取 `ironic kernel` 以及 `initramfs` 镜像。并且配置 `ceph` 的信息。

```console
root@kolla-ansible-w:~# mkdir -p /etc/kolla/config/ironic
root@kolla-ansible-w:~# wget https://seafile.sh.99cloud.net/seafhttp/files/59d1a22b-cbb2-4a84-816b-d4d424c12e79/ironic-agent.kernel -O /etc/kolla/config/ironic/ironic-agent.kernel
root@kolla-ansible-w:~# wget https://seafile.sh.99cloud.net/seafhttp/files/9c6caedb-4d84-47e1-aaf8-4e02dceaab80/ironic-agent.initramfs -O /etc/kolla/config/ironic/ironic-agent.initramfs
root@kolla-ansible-w:~# mkdir -p /etc/kolla/config/glance
root@kolla-ansible-w:~# ssh root@172.16.150.59 sudo tee /etc/ceph/ceph.conf </etc/kolla/config/glance/ceph.conf
root@kolla-ansible-w:~# ceph auth get-or-create client.glance | ssh root@172.16.150.59 sudo tee /etc/kolla/config/glance/ceph.client.glance.keyring
root@kolla-ansible-w:~# mkdir -p /etc/kolla/config/nova
root@kolla-ansible-w:~# ssh root@172.16.150.59 sudo tee /etc/ceph/ceph.conf </etc/kolla/config/nova/ceph.conf
root@kolla-ansible-w:~# ceph auth get-or-create client.cinder | ssh root@172.16.150.59 sudo tee /etc/kolla/config/nova/ceph.client.cinder.keyring
root@kolla-ansible-w:~# ceph auth get-or-create client.nova | ssh root@172.16.150.59 sudo tee /etc/kolla/config/nova/ceph.client.nova.keyring
root@kolla-ansible-w:~# mkdir -p /etc/kolla/config/cinder
root@kolla-ansible-w:~# ssh root@172.16.150.59 sudo tee /etc/ceph/ceph.conf </etc/kolla/config/cinder/ceph.conf
root@kolla-ansible-w:~# mkdir -p /etc/kolla/config/cinder/cinder-volume
root@kolla-ansible-w:~# ceph auth get-or-create client.cinder | ssh root@172.16.150.59 sudo tee /etc/kolla/config/cinder/cinder-volume/ceph.client.cinder.keyring
root@kolla-ansible-w:~# mkdir -p /etc/kolla/config/cinder/cinder-backup
root@kolla-ansible-w:~# ceph auth get-or-create client.cinder | ssh root@172.16.150.59 sudo tee /etc/kolla/config/cinder/cinder-backup/ceph.client.cinder.keyring
root@kolla-ansible-w:~# ceph auth get-or-create client.cinder-backup | ssh root@172.16.150.59 sudo tee /etc/kolla/config/cinder/cinder-backup/ceph.client.cinder-backup.keyring
```

### 部署

1. `openstack` 部署

```console
root@kolla-ansible-w:~# kolla-ansible octavia-certificates
root@kolla-ansible-w:~# cd /opt/kolla-ansible/tools
root@kolla-ansible-w:~# ./kolla-ansible -i /opt/all-in-one bootstrap-servers
root@kolla-ansible-w:~# ./kolla-ansible -i /opt/all-in-one prechecks -e 'ansible_python_interpreter=/path/to/venv/bin/python3'
root@kolla-ansible-w:~# ./kolla-ansible -i /opt/all-in-one deploy -e 'ansible_python_interpreter=/path/to/venv/bin/python3'
root@kolla-ansible-w:~# ./kolla-ansible post-deploy
```

2. 安装 `opesntack` 客户端

```console
# 安装客户端
root@kolla-ansible-w:~# pip install -i https://pypi.douban.com/simple/ python-openstackclient
# 把admin用户信息添加到环境变量中
root@kolla-ansible-w:~# . /etc/kolla/admin-openrc.sh
# 创建示范网络和下载所需要的测试镜像
root@kolla-ansible-w:~# /opt/kolla-ansible/tools/init-runonce
```

3. 上传 octavia amphora 镜像

```console
root@kolla-ansible-w:~# wget https://seafile.sh.99cloud.net/seafhttp/files/6a46def3-b04b-491b-9018-afbedbf8907f/amphora-x64-haproxy.qcow2
root@kolla-ansible-w:~# source /etc/kolla/octavia-openrc.sh
root@kolla-ansible-w:~# openstack image create amphora-x64-haproxy.qcow2 --container-format bare --disk-format qcow2 --private --tag amphora --file amphora-x64-haproxy.qcow2 --property hw_architecture='x86_64' --property hw_rng_model=virtio
```

4. 修改 `octavia` 使用的 `net`

```console
root@kolla-ansible-w:~# source /etc/kolla/admin-openrc.sh
root@kolla-ansible-w:~# openstack router delete demo-router
root@kolla-ansible-w:~# openstack network delete public1
root@kolla-ansible-w:~# OCTAVIA_MGMT_SUBNET=192.168.200.0/24
root@kolla-ansible-w:~# OCTAVIA_MGMT_SUBNET_START=192.168.200.210
root@kolla-ansible-w:~# OCTAVIA_MGMT_SUBNET_END=192.168.200.220
root@kolla-ansible-w:~# source /etc/kolla/octavia-openrc.sh
root@kolla-ansible-w:~# openstack network create public1 --provider-network-type flat --provider-physical-network physnet1 --external --share
root@kolla-ansible-w:~# openstack subnet create --subnet-range $OCTAVIA_MGMT_SUBNET --allocation-pool start=$OCTAVIA_MGMT_SUBNET_START,end=$OCTAVIA_MGMT_SUBNET_END --network public1 subnet
root@kolla-ansible-w:~# NET_NETWORK_ID=`openstack network show public1 -f value -c id`
root@kolla-ansible-w:~# sed -i "s/^amp_boot_network_list = *.*/amp_boot_network_list = $NET_NETWORK_ID/g" /etc/kolla/octavia-api/octavia.conf
root@kolla-ansible-w:~# sed -i "s/^amp_boot_network_list = *.*/amp_boot_network_list = $NET_NETWORK_ID/g" /etc/kolla/octavia-health-manager/octavia.conf
root@kolla-ansible-w:~# sed -i "s/^amp_boot_network_list = *.*/amp_boot_network_list = $NET_NETWORK_ID/g" /etc/kolla/octavia-housekeeping/octavia.conf
root@kolla-ansible-w:~# sed -i "s/^amp_boot_network_list = *.*/amp_boot_network_list = $NET_NETWORK_ID/g" /etc/kolla/octavia-worker/octavia.conf
root@kolla-ansible-w:~# docker restart octavia_api octavia_health_manager octavia_housekeeping octavia_worker
```

5. 上传 `ironic kernel` 和 `initramfs` 镜像

```console
root@kolla-ansible-w:~# source /etc/kolla/admin-openrc.sh
root@kolla-ansible-w:~# openstack image create --disk-format ari --container-format ari --public --file /etc/kolla/config/ironic/ironic-agent.initramfs deploy-initrd
root@kolla-ansible-w:~# openstack image create --disk-format aki --container-format aki --public --file /etc/kolla/config/ironic/ironic-agent.kernel deploy-vmlinuz
```

### 部署 `skyline`

直接使用提供的 `skyline` 镜像，详细的部署流程参考数据库使用 `mariaDB` 部署，文档地址为
<https://opendev.org/skyline/skyline-apiserver/src/branch/master/README-zh_CN.md>

启动容器后根据实际环境修改 `/etc/skyline/skyline.yaml` ，修改完毕查看 `skyline` 容器日志判断服务是否正常运行，如果出现 401 权限校验问题查看
`system_user_password` 是否正确，出现 `url` 问题把 `localhost` 改为本机的 `ip` 地址，出现数据库问题查看 `database_url` 是否配置正确

## 修改参考

### 添加企业的 `openstack-exporter`

添加云主机 `top 5` 的 `metric`, 把企业的 `openstack-exporter` 镜像添加到装有社区版的环境中

#### 修改企业 `openstack-exporter` 的配置文件

1. 创建 `openstack-exporter` 配置文件目录

```console
root@kolla-ansible-w:~# mkdir -p /etc/openstack-exporter
```

2. 添加配置文件

```console
# /etc/openstack-exporter/uwsgi.ini
root@kolla-ansible-w:~# cat <<EOF> /etc/openstack-exporter/uwsgi.ini
[uwsgi]
http = 192.168.100.149:9183
module = openstack_exporter.main:app
callable = app
processes = 1
threads = 10
stats = 192.168.100.149:9185
EOF

# /etc/openstack-exporter/openstack_exporter.conf
root@kolla-ansible-w:~# cat <<EOF> /etc/openstack-exporter/openstack_exporter.conf
[DEFAULT]
address = "192.168.100.149" 
port = "9183" 

[keystone_authtoken]
auth_type = "password" 
auth_url = "http://192.168.100.149:5000/v3" 
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
root@kolla-ansible-w:~# cat <<EOF> /etc/kolla/prometheus-server/openstack_exporter.rules
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
```

4. 在 `/etc/kolla/prometheus-server/prometheus.yml` 配置文件中增加配置

```yaml
rule_files:
  - /etc/prometheus/openstack_exporter.rules
```

5. 启动 `openstack-exporter` 服务

```console
root@kolla-ansible-w:~# docker run -d --name openstack_exporter --pid=host --privileged --restart=always -v /etc/openstack-exporter:/etc/openstack-exporter -v /etc/localtime:/etc/localtime -v /run/libvirt:/run/libvirt -v /etc/pki:/etc/pki -v /run/netns:/run/netns -v /run/openvswitch:/run/openvswitch --net=host openstack-exporter/openstack-exporter:latest uwsgi --ini /etc/openstack-exporter/uwsgi.ini
```

6. 在 `[rbd-1]` 配置项下新增配置

```console
rbd_exclusive_cinder_pool = False
```

7. 重启容器

```console
root@kolla-ansible-w:~# docker restart prometheus-server cinder_volume openstack_exporter
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

1. 修改 `heat` 服务中 `/v1/{tenant_id}/stacks` 接口的访问权限，修改后如下

```yaml
# List stacks globally.
# GET  /v1/{tenant_id}/stacks
# Intended scope(s): system, project
# "stacks:global_index": "role:reader and system_scope:all"
"stacks:global_index": "role:admin"
```

2. 重启 `heat` 服务

```console
root@kolla-ansible-w:~# docker restart heat-api
```

# kolla-ansible 部署基于 Wallaby 版本的 OpenStack

## 涵盖组件

| 组件名        | 描述             |
| ---------- | -------------- |
| horizon    | 社区 dashboard   |
| keystone   | 认证鉴权等管理        |
| glance     | 镜像等管理          |
| cinder     | 块存储等管理         |
| nova       | 虚拟机等管理         |
| neutron    | 网络，qos，vpn 等管理 |
| octavia    | LB 等管理         |
| ironic     | 裸机等管理          |
| prometheus | 监控等管理          |
| skyline    | 社区新 dashboard  |

## 准备工作

_如果是在云平台上部署，那么首先可以创建两个租户网络（即业务网）以及一个路由器并且开启公网网关。并且将两个租户网络绑定至路由器上。_

网络01：net01 子网01：subnet01 192.168.100.0/24

网络02：net02 子网02：subnet02 192.168.200.0/24

路由器01：R01 将 subnet01 以及 subnet02 绑定至 R01 上。

**以下内容均在当前网络规划下进行，在实际参考过程中，请按实际的网络做相应的修改。**

## 开始部署

### 存储集群 - 外置 ceph 集群

#### 环境准备

一台服务器：

- OS：`ubuntu 18.04 LTS`
- 一块网卡：net01 192.168.100.179
- 浮动 IP：绑定至 net01 上，172.16.150.59
- 二块数据盘：作为 OSD 盘

#### 部署 ceph

部署的是 ceph nautilus 版本。

具体步骤略，可以[参考官方部署 ceph-deploy](https://docs.ceph.com/en/nautilus/start/)

#### 验证 ceph 集群

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

**待后续 OpenStack 集群部署时，使用 ceph 集群信息。**

### OpenStack 集群部署 - Wallaby 版

#### 环境准备

一台服务器：

- OS：`ubuntu 20.04 LTS`
- 两块网卡：net01 192.168.100.149 net02 192.168.200.162
- 浮动 IP：绑定至 net01 上，172.16.150.77

**关闭两块网卡的安全组，即关闭端口安全。**

#### 开始部署

部署的是 OpenStack Wallaby 版本。

具体步骤略，可以[参考官方部署 kolla-ansible](https://docs.openstack.org/kolla-ansible/wallaby/user/quickstart.html)

附上 `globals.yml` 配置详情。

- `globals.yml` 配置见如下，下述为文件中打开的选项：

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
enable_haproxy: "no"
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
ironic_dnsmasq_dhcp_range: "192.168.100.210,192.168.100.220,255.255.255.0"
ironic_cleaning_network: "public1"

octavia_auto_configure: "yes"
octavia_amp_image_tag: "amphora"
octavia_loadbalancer_topology: "SINGLE"
```

获取 ironic kernel 以及 initramfs 镜像，并且配置 ceph 的信息。

```console
mkdir -p /etc/kolla/config/ironic
mkdir -p /etc/kolla/config/glance
mkdir -p /etc/kolla/config/nova
mkdir -p /etc/kolla/config/cinder
mkdir -p /etc/kolla/config/cinder/cinder-volume
mkdir -p /etc/kolla/config/cinder/cinder-backup
```

在 seafile 的 公共/产品部资料/Animbus IaaS产品资料/Ironic_deploy-images/x86 目录中下载 ironic-agent.kernel 和
ironic-agent.initramfs 放入/etc/kolla/config/ironic/ 目录

以下操作在 ceph 节点进行

```
# glance 配置
ssh root@172.16.150.77 sudo tee /etc/kolla/config/glance/ceph.conf </etc/ceph/ceph.conf
ceph auth get-or-create client.glance | ssh root@172.16.150.77 sudo tee /etc/kolla/config/glance/ceph.client.glance.keyring

# nova 配置
ssh root@172.16.150.77 sudo tee /etc/kolla/config/nova/ceph.conf </etc/ceph/ceph.conf
ceph auth get-or-create client.cinder | ssh root@172.16.150.77 sudo tee /etc/kolla/config/nova/ceph.client.cinder.keyring
ceph auth get-or-create client.nova | ssh root@172.16.150.77 sudo tee /etc/kolla/config/nova/ceph.client.nova.keyring

# cinder 配置
ssh root@172.16.150.77 sudo tee /etc/kolla/config/cinder/ceph.conf </etc/ceph/ceph.conf
ceph auth get-or-create client.cinder | ssh root@172.16.150.77 sudo tee /etc/kolla/config/cinder/cinder-volume/ceph.client.cinder.keyring
ceph auth get-or-create client.cinder | ssh root@172.16.150.77 sudo tee /etc/kolla/config/cinder/cinder-backup/ceph.client.cinder.keyring
ceph auth get-or-create client.cinder-backup | ssh root@172.16.150.77 sudo tee /etc/kolla/config/cinder/cinder-backup/ceph.client.cinder-backup.keyring
```

开始部署

```console
root@kolla-ansible-w:~# kolla-genpwd
root@kolla-ansible-w:~# kolla-ansible octavia-certificates
root@kolla-ansible-w:~# kolla-ansible -i all-in-one bootstrap-servers
root@kolla-ansible-w:~# kolla-ansible -i all-in-one prechecks
root@kolla-ansible-w:~# kolla-ansible -i all-in-one deploy
root@kolla-ansible-w:~# pip install python-openstackclient
root@kolla-ansible-w:~# kolla-ansible post-deploy
root@kolla-ansible-w:~# source /etc/kolla/admin-openrc.sh
root@kolla-ansible-w:~# /usr/local/share/kolla-ansible/init-runonce
```

上传 octavia amphora 镜像

在 seafile 的 公共/产品部资料/Animbus IaaS产品资料/Octavia_deploy-images/octavia 目录中下载 amphora-x64-haproxy.qcow2

```console
root@kolla-ansible-w:~# source /etc/kolla/octavia-openrc.sh
root@kolla-ansible-w:~# openstack image create amphora-x64-haproxy.qcow2 --container-format bare --disk-format qcow2 --private --tag amphora --file amphora-x64-haproxy.qcow2 --property hw_architecture='x86_64' --property hw_rng_model=virtio
```

修改 octavia 使用的 net

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

上传 ironic kernel 和 initramfs 镜像

```console
root@kolla-ansible-w:~# source /etc/kolla/admin-openrc.sh
root@kolla-ansible-w:~# openstack image create --disk-format ari --container-format ari --public --file /etc/kolla/config/ironic/ironic-agent.initramfs deploy-initrd
root@kolla-ansible-w:~# openstack image create --disk-format aki --container-format aki --public --file /etc/kolla/config/ironic/ironic-agent.kernel deploy-vmlinuz
```

### vBMC - 虚拟裸机【可选】

#### 环境准备

一台服务器：

- OS：`CentOS 7.9.2009`
- 两块网卡：net01 192.168.100.177 net02 192.168.200.173
- 浮动 IP：绑定至 net01 上，172.16.150.100

**关闭两块网卡的安全组，即关闭端口安全。**

#### 部署 vBMC

参考项目：http://gitlab.sh.99cloud.net/shaleijie/ironic-ci-cd

```console
[root@vbaremetal ~]# git clone http://gitlab.sh.99cloud.net/shaleijie/ironic-ci-cd.git
[root@vbaremetal ~]# cd ironic-ci-cd/
[root@vbaremetal ~]# chmod +x create-node.sh enroll_nodes.sh main.sh setup-network.sh
[root@vbaremetal ~]# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
[root@vbaremetal ~]# pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
[root@vbaremetal ~]# scp -r root@192.168.100.149:/etc/kolla/ /etc/
[root@vbaremetal ~]# cd ironic-ci-cd/
[root@vbaremetal ~]# bash main.sh
```

验证 vBMC

```console
[root@vbaremetal ~]# virsh list --all
 Id    名称                         状态
----------------------------------------------------
 -     node-0                         关闭
 -     node-1                         关闭
 -     node-2                         关闭
[root@vbaremetal ~]# vbmc list
+-------------+---------+---------+------+
| Domain name | Status  | Address | Port |
+-------------+---------+---------+------+
| node-0      | running | ::      | 6230 |
| node-1      | running | ::      | 6231 |
| node-2      | running | ::      | 6232 |
+-------------+---------+---------+------+
```

enroll 虚拟裸机

```console
[root@vbaremetal ironic-ci-cd]# HOST_ip="<vBMC_IP>"
[root@vbaremetal ironic-ci-cd]# sed -i "s/^HOST_IP=*.*/HOST_IP=\"$HOST_IP\"/g" enroll_nodes.sh
[root@vbaremetal ironic-ci-cd]# ./enroll_nodes.sh
```

等待 enroll 完成。登录 horizon 界面，在管理平台中，更新裸机的 kernel 以及 initramfs 镜像信息。

### 部署 skyline

#### 构建 skyline 镜像

使用此 [Dockerfile](https://opendev.org/skyline/skyline-apiserver/src/branch/master/container) 构建镜像。

#### 开始部署 skyline

参考此[文档](https://opendev.org/skyline/skyline-apiserver/src/branch/master/README-zh_CN.md#%E9%83%A8%E7%BD%B2-%E6%95%B0%E6%8D%AE%E5%BA%93%E4%BD%BF%E7%94%A8-mariadb)。

## 登录 skyline

访问：https://172.16.150.77:9999

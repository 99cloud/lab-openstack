# OpenStack 实操进阶

## 注意 ⚠️

- *斜体表示引用*
- **未经允许，禁止转载**

## Prerequisite

- vim 基础操作 -- 编辑、修改、保存文件
- 网络基础知识 -- 网段 cidr、vlan、vxlan、配置 linux 网卡等等
- 基础的 linux 知识 -- 权限、文件系统、服务
- systemd 的基础操作 -- 重启、关闭、启动、重载、查看 systemd 的服务

## 课程目录

| 日程    | 时间 | 课程              | 内容                |
| ------ | ---- | ---------------- | ------------------ |
| 第 1 天 | 上午 | [基础](#1-基础)    | [1.1 简介](#11-简介) |
|        |      |                  | [1.2 Keystone](#12-keystone) |
|        |     |                   | [1.3 Horizon](#13-horizon) |
|        | 下午 |                   | [1.4 Nova](#14-nova) |
|        |     |                   | [1.5 Glance](#15-glance) |
|        |     |                   | [1.6 Cinder](#16-cinder) |
| 第 2 天 | 上午 |                  | [1.7 Neutron](#17-neutron) |
|        | 下午 | [部署](#2-部署)    | [2.1 部署前准备](#21-部署前准备) |
|        |     |                   | [2.2 DevStack](#22-devstack) |
|        |     |                   | [2.3 Kolla Ansible](#23-kolla-ansible) |
| 第 3 天 | 上午 | [运维](#3-运维)    | [3.1 OpenStack Ansible](#31-openstack-ansible) |
|        |     |                   | [3.2 小版本升级](#32-小版本升级) |
|        |     |                   | [3.3 扩缩容](#33-扩缩容) |
|        | 下午 |                   | [3.4 基础组件运维](#34-基础组件运维) |
|        |     | [排错](#4-排错)    | [4.1 日志查询](#41-日志查询) |
|        |     |                   | [4.2 服务异常检测](#42-服务异常检测) |
|        |     |                   | [4.3 存储异常](#43-存储异常) |
|        |     |                   | [4.4 网络异常](#44-网络异常) |

## 1. 基础

[返回目录](#课程目录)

### 1.1 简介

[返回目录](#课程目录)

参考：[OpenStack 概述](class-01-OpenStack-Administration.md#2-openstack-概述)

### 1.2 Keystone

[返回目录](#课程目录)

参考：[身份认证服务 - Keystone](class-01-OpenStack-Administration.md#3-keystone)

### 1.3 Horizon

[返回目录](#课程目录)

参考：[看板服务 - Horizon](class-01-OpenStack-Administration.md#4-horizon)

### 1.4 Nova

[返回目录](#课程目录)

参考：[计算服务 - Nova](class-01-OpenStack-Administration.md#5-nova)

### 1.5 Glance

[返回目录](#课程目录)

参考：[镜像服务 - Glance](class-01-OpenStack-Administration.md#6-glance)

### 1.6 Cinder

[返回目录](#课程目录)

参考：[块存储 - Cinder](class-01-OpenStack-Administration.md#7-cinder)

### 1.7 Neutron

[返回目录](#课程目录)

参考：[网络服务 - Neutron](class-01-OpenStack-Administration.md#8-neutron)

## 2. 部署

[返回目录](#课程目录)

### 2.1 部署前准备

[返回目录](#课程目录)

**基础环境安装**，参考：[Github](https://github.com/wu-wenxiang/lab-kubernetes/blob/main/doc/kubernetes-best-practices.md#111-%E5%86%85%E6%A0%B8%E5%8D%87%E7%BA%A7) 或 [Gitee](https://gitee.com/wu-wen-xiang/lab-kubernetes/blob/main/doc/kubernetes-best-practices.md#111-%E5%86%85%E6%A0%B8%E5%8D%87%E7%BA%A7)

### 2.2 DevStack

[返回目录](#课程目录)

参考：[DevStack 部署环境](devstack-aio.md)

### 2.3 Kolla Ansible

[返回目录](#课程目录)

参考：[Wallaby 版本 Kolla Ansible 部署](kolla/kolla-ansible-wallaby.md)

## 3. 运维

[返回目录](#课程目录)

### 3.1 OpenStack Ansible

[返回目录](#课程目录)

参考：[OpenStack Ansible 组件](class-02-OpenStack-API-and-Development.md#openstack-ansible-provider--catalog-)

### 3.2 小版本升级

[返回目录](#课程目录)

### 3.3 扩缩容

[返回目录](#课程目录)

### 3.4 基础组件运维

[返回目录](#课程目录)

#### 3.4.1 MariaDB

[返回目录](#课程目录)

MariaDB 的一般操作：

1. 检查和判断数据库服务是否健康

查看 docker 状态及 log

```
docker ps|grep mariadb
docker logs mariadb
```

查看系统状态

```
docker exec -it mariadb bash
mysql -u root -p
SHOW GLOBAL STATUS;
```

查看缓存状态

```
SHOW STATUS LIKE 'Qcache%';
```

1. 备份 & 恢复

备份

```
mkdir –p /opt/mariadb-backup
cp –rf /var/lib/docker/volumes/mariadb/ /opt/mariadb-backup
```

恢复

将 /opt/mariadb-backup 恢复至 mariadb 挂载目录即可

1. HA & 部分节点下线后修复

MariaDB 支持 ha，采用 galera cluster 多主结构，通过 sst(State Snapshot Transfer) 同步数据

可在 mariadb 配置文件 galera.cnf 查看具体配置信息

```
wsrep_sst_method = mariabackup
wsrep_on = ON
```

查看集群状态

```
SHOW GLOBAL STATUS LIKE 'wsrep%';
```

- wsrep_cluster_state_uuid: 集群的 state UUID
- wsrep_cluster_size: 集群中节点的个数
- wsrep_cluster_status: 集群里节点的主状态
- wsrep_ready: 节点是否可以接受 query
- wsrep_connected: 节点的网络连接
- wsrep_local_state_comment: 节点的状态

查看 grastate.dat，一般文件路径为 /var/lib/docker/volumes/mariadb/_data/grastate.dat，
如果该节点数据库服务正在运行，则 seqno 值为 -1

```
# GALERA saved state
version: 2.1
uuid:    4776eea5-fc98-11ec-9bac-26114b55c543
seqno:   -1
safe_to_bootstrap: 0
```

如果某节点数据库服务停止运行，则 seqno 值改变，如：

```
# GALERA saved state
version: 2.1
uuid:    4776eea5-fc98-11ec-9bac-26114b55c543
seqno:   342591
safe_to_bootstrap: 0
```

如果集群只剩下一个节点数据库服务正常运行，则该正常运行的节点 safe_to_bootstrap 值变为 1，如：

```
# GALERA saved state
version: 2.1
uuid:    4776eea5-fc98-11ec-9bac-26114b55c543
seqno:   -1
safe_to_bootstrap: 1
```

如果集群所有节点同时崩溃，所有节点的 grastate.dat 文件 safe_to_bootstrap 值全部为 0，则会造成集群无法启动

1. 断电自动修复

- 若只有部分节点故障，一般只需要重启该节点即可

- 若全部节点同时断电故障，则需要选择最新节点作为集群启动节点来恢复

    备份所有节点数据

    ```
    mkdir –p /opt/mariadb-backup
    cp –rf /var/lib/docker/volumes/mariadb/ /opt/mariadb-backup
    ```

    选取所有节点 grastate.dat 文件中 seqno 值最大的为启动节点

    若所有节点 seqno 均为 -1，则选取 gvwstate.dat 文件中 my_uuid 值与 view_id 值相等的为启动节点

    将选取的启动节点先行启动，再依次恢复其余节点，查看集群状态，确保 mariadb 集群已正常启动

#### 3.4.2 RabbitMQ

[返回目录](#课程目录)

1. 检查和判断消息队列是否健康

查看 docker 状态及 log

```
docker ps|grep rabbitmq
docker logs rabbitmq
```

查看 rabbitmq 状态

```
docker exec -it rabbitmq rabbitmqctl status
```

查看 rabbitmq 集群状态

```
docker exec -it rabbitmq rabbitmqctl cluster_status
```

查看 rabbitmq 管理界面 `http://<ip>:15672`
默认用户名及密码均为`guest`

1. 常见错误和修复方法

- 若 rabbitmq 未开启管理界面，则需要执行以下命令

    ```
    rabbitmq-plugins enable rabbitmq_management
    ```

- 若使用 guest 账号登录提示 `User can only log in via localhost`，则需配置一个允许远程访问的用户

    ```
    rabbitmqctl add_user <username> <password>
    rabbitmqctl set_user_tags <username> administrator
    rabbitmqctl set_permissions -p "/" <username> ".*" ".*" ".*"
    ```

- 若 rabbitmq 服务报错

    ```
    docker restart rabbitmq
    docker logs rabbitmq
    ```

    查看日志 /var/log/kolla/rabbitmq，分析错误原因

#### 3.4.3 Prometheus

[返回目录](#课程目录)

参考 [监控和告警](class-03-OpenStack-Maintenance.md#4-监控和告警)

#### 3.4.4 EFK

[返回目录](#课程目录)

参考 [ElasticSearch](class-03-OpenStack-Maintenance.md#8-elastic-search)

## 4. 排错

[返回目录](#课程目录)

### 4.1 日志查询

[返回目录](#课程目录)

参考 [Cinder 服务报错排错](class-01-OpenStack-Administration.md#94-debug-cinder)

参考 [老版本中 Python2 中文处理问题](http://blog.wuwenxiang.net/OpenStack-Debug)

### 4.2 服务异常检测

[返回目录](#课程目录)

1. 如何检查和判断 OpenStack 服务发生异常？

查看 docker 状态及 log

```
docker ps|grep <server>
docker logs <sever>
```

尝试 curl API，查看返回值是否正常，API 详情:[openstack API 文档](https://docs.openstack.org/zh_CN/api-quick-start/)

查看组件日志 /var/log/kolla/<server>，是否有 ERROR 报错

1. 一般错误和修复方案

重启 docker

```
docker restart <server>
```

开启组件 LOG DEBUG 配置，查看日志详情分析错误原因

### 4.3 存储异常

[返回目录](#课程目录)

1. 如何检查和判断 Ceph 发生异常？

查看 docker 状态

```
docker ps -a|grep ceph 
```

health 检查

```
ceph health
```

查看 ceph 状态

```
ceph status
```

查看 mon 状态

```
ceph mon stat
```

使用状态检查

```
ceph osd df
ceph df
```

1. 一般错误和修复方案

- 查看 ceph 健康状态时报错 HEALTH_WARN mons are allowing insecure global_id reclaim

    禁用不安全模式
    
    ```
    ceph config set mon auth_allow_insecure_global_id_reclaim false
    ```

- ceph 集群报错 daemons have recently crashed

    ceph 归档检查

    ```
    ceph crash ls
    ceph crash archive <id>
    ceph crash archive-all
    
    ceph -s
    ```

- ceph osd 空间不足

    尝试释放部分磁盘空间或部署新的 osd 以增加磁盘空间

    数据平衡
    
    ```
    ceph osd crush reweight <osd> <weight>
    ```

### 4.4 网络异常

[返回目录](#课程目录)

1. 如何检查和判断基础网络发生异常？如何修复

查看网络组件状态和 log，若有异常状态，则重启对应组件

```
openstack network list
openstack network agent list
```

测试基础网络是否互通，若所有路由均异常，则尝试重启如下组件修复

```
docker restart neutron_l3_agent neutron_dhcp_agent
```

1. 如何检查和判断租户网络发生异常？如何修复

查看 neutron log 记录，是否有 ERROR 记录

若为某网络路由 ERROR，则尝试重建对应路由等

若路由正常，查看虚机内网络 ifconfig 和路由 route 状态，尝试修复虚机路由或手动启动 dhcp

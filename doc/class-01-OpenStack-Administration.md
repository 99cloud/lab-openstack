# OpenStack-Administration

## Prefix

- 授课时长：
    - 上午：9:30 至 11:30
    - 下午：13:30 至 16:30
- Prerequisite
    - vim 基础操作 -- 编辑、修改、保存文件
    - 网络基础知识 -- 网段 cidr、vlan、vxlan、配置 linux 网卡等等
    - 基础的 linux 知识 -- 权限、文件系统、服务
    - systemd 的基础操作 -- 重启、关闭、启动、重载、查看 systemd 的服务

## Catalog

| Date | Time | Title | Content |
| ---- | ---- | ----- | ------- |
| 第 1 天 | 上午 | [1. OpenStack 概述]() | [OpenStack 从何而来？]() |
| | | | [OpenStack 的组件架构是怎样的？]() |
| | | | [云计算的技术发展趋势是怎样的？]() |
| | | | [OpenStack 的参考资料有哪些？]() |
| | | [Lesson 02：管理身份认证服务 - Keystone](#) | [Keystone 的概念空间中有哪些对象？](#) |
| | | | [Keystone 能提供哪些服务？]() |
| | 下午 | [Lesson 03：管理看板服务 - Horizon]() | [如何通过 Dashboard 来管理 OpenStack 平台？](#) |
| | | | [如何配置 Horizon 来⽀持多 Domain 登录？](#) |
| | | [Lesson 04：管理计算服务 - Nova](#) | [理解虚拟化](#) |
| | | | [学习规划硬件计算资源（ 算你需要买多少服务器 ）](#) |
| | | | [管理 flavor](#) |
| | | | [管理 compute instance（ 如启动、关闭、终⽌ ）](#) |
| | | | [管理Nova⽤户密钥对（ keypair ）](#) |
| | | | [启动⼀个新实例](#) |
| | | | [关闭⼀个实例](#) |
| | | | [终⽌实例](#) |
| | | | [配置⼀个拥有 floating IP 的实例]() |
| | | | [管理项⽬的安全组规则]() |
| | | | [分配安全组给实例]() |
| | | | [分配 floating IP 给实例]() |
| | | | [从实例上分离 floating IP]() |
| 第 2 天 | 上午 | | [理解虚拟机从镜像启动和从云盘启动的区别](#) |
| | | | [nova 管理虚拟机的静态数据的位置](#) |
| | | | [devstack 服务的管理](#) |
| | | [Lesson 05：管理镜像服务 - Glance](#) | [理解 OpenStack 中使⽤的镜像](#) |
| | | | [上传⼀个镜像](#) |
| | | | [管理镜像类型和后端](#) |
| | | | [管理镜像（ 如添加、更新、移除 ）](#) |
| | 下午 | [Lesson 06：管理块存储 - Cinder]() | [理解 Cinder 的作⽤](#) |
| | | | [统⼀的存储解决⽅案 Ceph 的简介](#) |
| | | | [管理卷](#) |
| | | | [创建块存储的卷组](#) |
| | | | [创建⼀个新的卷并将其安装到 Nova 实例上](#) |
| | | | [管理配额](#) |
| | | | [管理卷的配额](#) |
| | | | [管理卷的备份](#) |
| | | | [备份和恢复卷](#) |
| | | [Lesson 07：管理对象存储 - Swift](#) | [理解 Swift 的使⽤场景](#) |
| | | | [Ring 的设计简介](#) |
| | | | [管理对象存储的](#) |
| | | | [管理到期的对象](#) |
| | | [Lesson 08：管理⽹络服务 - Neutron](#) | [理解 Neutron 的作⽤](#) |
| | | | [⽣产环境中的实施⽅案](#) |
| | | | [⽹络加速的技术 dpdk、sr-iov 的介绍](#) |
| | | | [理解节点的内部⽹络的实现](#) |
| | | | [管理⽹络资源（ 如路由、⼦⽹ ）](#) |
| | | | [创建外部⽹络](#) |
| | | | [创建路由](#) |
| | | | [在虚拟环境中管理⽹络服务](#) |
| | | | [管理安全组规则](#) |
| 第 3 天 | 上午 | [Lesson 09：编排服务 - Heat](#) | [Heat 的模版中的讲解](#) |
| | | | [通过⼀个模版创建 OpenStack 的资源](#) |
| | | | [更新⼀个模版](#) |
| | | | [创建互相依赖 yaml 模版]() |
| | 下午 | [Lesson 10：模拟管理员练习题]() | [模拟题讲解](#) |
| | | | [模拟题练习]() |

## Lesson 01：OpenStack Introduction ( [Catalog](#catalog) )

云计算最初的概念是”网络即是电脑”, 尔后 Amazon 推出的弹性云计算 (EC2) 提供用户使用资源并且收费, 大致顶定了云计算的商业用途。OpenStack 是一个开源的云平台, 他属于云计算当中我们常说的IAAS(infrastructure as a service),简单的讲他是来管理我们的硬件设施的, 我们在我们的设备上部署Linux与OpenStack, 然后由 OpenStack 来帮助我们决定哪些虚拟机应该启动在哪些物理的计算节点上

    ![simpleOpenstackArch](../img/simpleOpenstackArch.png)
    
    ![iaas](../img/iaas.png)

### Virtualization & OpenStack ( [Catalog](#catalog) )

1. 什么是虚拟化？虚拟化的发展历程如何？60-70 IBM / 80-90 VMWare / 2005-2010 Amazon / 2010 NASA Nebula & RackSpace Cloud Storage
1. 云计算的类型有几种类型？IaaS / PaaS / SaaS，只有 IaaS 是必须基于虚拟化的

### OpenStack Infrastructure ( [Catalog](#catalog) )

1. OpenStack 哪些是核心项目？Keystone / Nova / Cinder / Neutron / Glance
1. [Design](https://docs.openstack.org/arch-design/design.html)

    ![](https://docs.openstack.org/arch-design/_images/osog_0001.png)

1. [Logical architecture](https://docs.openstack.org/install-guide/get-started-logical-architecture.html)

    ![](../img/openstack-arch-kilo-logical-v1.png)

1. [Conceptual architecture](https://docs.openstack.org/ocata/admin-guide/common/get-started-conceptual-architecture.html)

    ![](https://docs.openstack.org/ocata/admin-guide/_images/openstack_kilo_conceptual_arch.png)

1. OpenStack 的发展过程？模块化 & 服务化，核心项目 & 集成项目 => Big Tent
1. 平均6个月版本更新, 每个版本维护18个月, bugfix

1. [stackalytics](https://www.stackalytics.com/)

1. [Source code](https://opendev.org/openstack)

1. [launchpad](https://bugs.launchpad.net/)

1. [review](https://review.opendev.org/)

    ![](../img/qualityfordevelop.png)

### The Trend of Cloud Computing ( [Catalog](#catalog) )

1. 私有云、公有云、混合云的发展趋势如何？Azure / Aliyun / HW
1. IaaS & CaaS 谁会是未来的主流？
1. OpenStack 的发展趋势？

裸机资源的管理: 
        Ironic 裸机节点纳管,精准的编排与调度,实现裸机云

容器化:
        Docker Containerd CRIO,到的Kubernetes容器管理平台,弥补openstack原生云
        kolla-ansible 布署容器化openstack
        openstack-helm 基于kubernetes管理平台部署openstack     

相容于主流资源池化:
        数据池化  SDS -- Ceph and Cinder-volume 
                高性能 高可用性 高可扩展性 支持三种存储接口(文件, 块, 物件)
        网络资源池化 SDN -- Neutron Server
                控制转发分离 集中控制 虚拟化

### OpenStack Reference ( [Catalog](#catalog) )

1. 官方文档在哪里？
1. 有哪些推荐的入门书？《每天五分钟玩转 OpenStack》，《OpenStack 设计与实现》

### reference ( [Catalog](#catalog) )

1. How openstack service implements communication?
1.   infra: restful api
1.   inner: message queue

    ![](../img/communication.png)

1. Restful api

OpenStack是由很多个核心组件组合而成，每个组件都负责他们自己的一小块的功能比如负责提供计算服务的是Nova，提供网络服务的是Neutron,他们各自都有属于自己的管理接口，所谓管理接口就是一个基于http请求的一个Web服务，主要是用于接受命令行工具或者组件的http请求。
访问管理接口的过程, 使用者发出请求(request)以RESTful的风格,基于http网络协议, 传送送到处理RESTful封包的接口, 又称REST API, 完成对数据库的增删查找.

    ![](../img/restfulapi.png)

1. Message queue

    ![](../img/rabbitmqex.png)
    ![](../img/rabbitmqex2.png)
    ![](../img/rabbitmqex3.png)

1. message for openstack oslo.messageing
Event Notification
    将讯息发送到总线上面, 对此类讯息感兴趣的服务进程会去获取此讯息, 做进一步的处理
    举例来说: 计量服务的Ceilometer就是监听总线获取其他服务的事件,进而实现计量与监控

Remote Procedure Call(RPC)
    Cast: 异步执行远程方法,调用者不会等待结果返回
    Call: 同步执行远程方法,调用者会等待结果返回

    ![](../img/oslo.png)

1. database and sqlachemy

Openstack以Python语法实现IaaS架构,在各组件调度资源的过程,需要一数据库记录所有平台管理资料
底层后台数据库琳琅满目 MySQL Mariadb PostgreSQL Sqlite3 等
上层开发需要使用Python语法实现
基于这样环境Openstack使用SQLAchemy来管理数据库
SQLAchemy是一个以Python语法写成向下对数据库键值进行修改的工具 

    ![](../img/sqlachemy.png)

## Lesson 02：Keystone

1. keystone 在 openstack 扮演什么角色
**用户的身份认证服务包括组件和组件之间的身份认证**
**为 OpenStack 提供目录服务**
**规则服务**

### Keystone Concepts

1. 什么是 User / Group / Project / Tenant / domain？
User: 最基本的用户, 一个通常意义上的账号有用户名和密码还有一些相关的比如邮件等信息, 在OpenStack中只是创建一个用户是不可以使用OpenStack中的资源的
group: 组顾名思义就是一个用户的集合, 一般我们会把一个用户关联到一个项目中, 每次关联的时候都要设置一个角色比较麻烦, 有了组以后我们可以把组加到租户当中去并关联一个角色, 以后所以加入到这个组当中的用户就继承了这个组在这个租户当中的角色
project/tenant: project顾名思义是项目的意思或者用我们熟知的话就是租户, 在本书中我们都会称之为项目而不是租户, 租户是OpenStack中一个核心的概念, 基本上所有的资源都是按照租户隔离, 比如网络、实例、路由等资源, 所以我们可以想象一个用户必须要先关联到一个项目中去才能正确使用OpenStack资源
domain: 在OpenStack当中域是用来实现真正的多项目/租户模>式的一种方法, 在没有域出现之前OpenStack有着一个权限的场景, 当你把一个用户任何一个项目/租户当中去的时候，你如果关联的是admin的角色的话, 这个时候这个用户突然就>成为了OpenStack超级管理员, 这并非我们所希望的场景, 使用了域以后我们就可以实现真>正意义上的多项目/租户模式了, 把一个用户加到default以外的域中的项目并关联到admin>的时候, 这个用户就不再是整个OpenStack的管理员了, 他只能管理这个域下面的所有的项目/租户, 当然你要开启多项目/租户模式你得替换掉/etc/keystone/policy.json文件来开启

    ![](../img/DomainUserProjectRole.png)

1. 什么是服务终端 service endpoint？
服务终点即一个服务提供的地址比如 http://192.168.100.20:5000/v3, 这就是一个服务终点, 服务终点是用来提供基于http请求的API方法的一个地址

1. 什么是目录服务？
之前提到OpenStack有很多个核心组件组合而成的, 每个组件都有一个或多个管理接口, 每个管理接口提供服务都是以web服务的形式出现的, 那么他们都有一个服务的终点地址比如keystone的(http://ip:5000/v3), 我们怎么才能找到每个组件的终端呢？因为这些服务可以很方便的迁移到任何网络可达的物理服务器上, 所有这里我们要一个机制来集中管理服务的终点, 就像服务终点的路由器一样, 更好理解的是像dns

1. 什么是 tokenid ? 
是缓存在服务器上的memcache中, 以减少数据库连接查询所带来的磁盘的io, 大大的提高了性能, 我们可以用类似的像postman等工具来查看api的返回结果

1. 什么是 Role / Policy？
keystone 遇到不同的使用者做出不同请求的问题 ( 例如: 创建虚拟机 删除云盘 ) 要透过 role 跟 policy 协作来满足需求, 每一个调度请求都会有一个对应的 policy 里面存有多向属性, 其中一个就是 role。 再来, 每个被创建的使用者都会被绑定一个 role (admin / member), 当使用者发出请求调度服务的时后, keystone 收到后会确认这个服务的policy role 是不是这个使用者可以有权利访问的, 如果有才可以继续, 反之拒绝

### Keystone Capablities

1. Keystone 怎么处理服务注册和服务发现？
练习: 如何添加一个新的服务终端?  
我们为 OpenStack 写了一个新的服务, 并且已经和开发团队约定好我们的服务以 Rest API 的方式部署, 我们的服务名称叫 myService, 我们的服务终端的地址为 http://172.25.0.10:3838。

```console
$ openstack service create --name myService --description "helloworld" myService
$ openstack endpoint create --region RegionOne myService public/internal/admin http://172.25.0.10:3838
```

1. Keystone 怎么处理组织和用户管理？用户、用户组、项目、配额
练习: 
```console
# 创建一个用户
$ openstack user create --password johnpassword john

# 更新一个用户
$ openstack user set --password newpassword john

# 删除一个用户
$ openstack user delete john

# 用户列表
$ openstack user list

# 查看详细
$ openstack user show john

# 将用户关联到项目/租户
$ openstack role add --user john --project demo admin 
```

1. Keystone 怎么处理认证、鉴权和授权？角色、RBAC、Cloud Admin / Domain Admin
练习: 只允许admin创建云盘
```console
# 检查/etc/cinder/ 路径下面有无policy,如果没有就新增一个
$ oslopolicy-sample-generator --namespace cinder --format json --output-file policy.json
$ sudo cp policy.json /etc/cinder/policy.json

# 添加或是修改policy路径到cinder.conf
[oslo_policy]
policy_file = /etc/cinder/policy.json

# 修改policy rule权限
"context_is_admin": "role:admin"
"network:create": "rule:context_is_admin",

# 重启服务
$ systemctl restart devstack@c-api
```

## Lesson 03：Horizon

### 检验 Dashboard 的运⾏

### 配置 Horizon 来⽀持多 Domain 登录

## Lesson 04：Nova

### 理解虚拟化

### 学习规划硬件计算资源（ 算你需要买多少服务器 ）

### 管理 flavor

### 管理 compute instance（ 如启动、关闭、终⽌ ）

### 管理Nova⽤户密钥对（ keypair ）

### 启动⼀个新实例

### 关闭⼀个实例

### 终⽌实例

### 配置⼀个拥有 floating IP 的实例

### 管理项⽬的安全组规则

### 分配安全组给实例

### 分配 floating IP 给实例

### 从实例上分离 floating IP

### 理解虚拟机从镜像启动和从云盘启动的区别

### nova 管理虚拟机的静态数据的位置

### devstack 服务的管理

## Lesson 05：Glance

### 理解 OpenStack 中使⽤的镜像

### 上传⼀个镜像

### 管理镜像类型和后端

### 管理镜像（ 如添加、更新、移除 ）

## Lesson 06：Cinder

### 理解 Cinder 的作⽤

### 统⼀的存储解决⽅案 Ceph 的简介

### 管理卷

1. cinder-volume 可以类比 nova-compute，运行在存储节点（ 定期主动上报容量 ）。cinder-api 运行在控制节点。cinder-schedule（ 默认用空闲容量计算权重 ）类比 nova-schedule（ 默认用空闲内存计算权重 ）。
1. cinder-provider（ 类比 hypervisor ）是独立的，cinder-volume 通过 driver（ 使用哪个 provider 通过 cinder.conf 确定 ） 和 provider 通信。如果有两个 provider，就需要两个不同的 cinder-volume。
1. Create Volume from Source：image / backup / snapshot ？ 增量还是全量？
1. Attach 方案就是 iSCSI，cinder-volume 初始化，nova-compute 来连接。
1. volume -> Image，可以
1. backup：容灾（ restore 是创建空白 volume & copy 数据过去 ），snapshot：便捷回溯
1. nova 的 snapshot 是对系统盘全量备份，生成 image 保存到 glance。Cinder 的 snapshot 依赖与 volume，有 snapshot 的 volume 不可以删除。通常 snapshot 和 volume 放在一起（ volume provider ）
1. NFS provider 里，volume 就是文件

### 创建块存储的卷组

### 创建⼀个新的卷并将其安装到 Nova 实例上

### 管理配额

### 管理卷的配额

### 管理卷的备份

### 备份和恢复卷

## Lesson 07：Swift

### 理解 Swift 的使⽤场景

### Ring 的设计简介

### 管理对象存储的

### 管理到期的对象

## Lesson 08：Neutron

### 理解 Neutron 的作⽤

### ⽣产环境中的实施⽅案

1. Linux Bridge 支持 vlan & vxlan

### ⽹络加速的技术 dpdk、sr-iov 的介绍

### 理解节点的内部⽹络的实现

### 管理⽹络资源（ 如路由、⼦⽹ ）

### 创建外部⽹络

### 创建路由

### 在虚拟环境中管理⽹络服务

### 管理安全组规则

### Debug

1. 场景：创建一个 port，固定 IP & MAC，MAC 11:22:33:44:55:66，创建 VM，指定这个 Port，会报错。

    ```bash
    journalctl -f -u devstack@n-cond.service
    journalctl -f -u devstack@n*
    journalctl -f -u devstack@n* > ~/a.txt
    ```

    ```
    Jul 28 16:48:10 test-coa-5 nova-conductor[7519]: 2020-07-28 16:48:10.626 8393 ERROR nova.scheduler.utils [req-9b59c38d-c943-4d56-82ca-5cf9f1b5bfe9 cee4ec5181d24cc2a3a3c4975c3277a2 4452a8c2601b482fb13639c8839c80f9 - default default] [instance: a5a972b4-b779-4931-94c3-c43956f4d7ee] Error from last host: test-coa-5 (node test-coa-5): [u'Traceback (most recent call last):\n', u'  File "/opt/stack/nova/nova/compute/manager.py", line 1996, in _do_build_and_run_instance\n    filter_properties)\n', u'  File "/opt/stack/nova/nova/compute/manager.py", line 2237, in _build_and_run_instance\n    instance_uuid=instance.uuid, reason=six.text_type(e))\n', u"RescheduledException: Build of instance a5a972b4-b779-4931-94c3-c43956f4d7ee was re-scheduled: XML error: expected unicast mac address, found multicast '11:22:33:44:55:66'\n"]
    ```

## Lesson 09：Heat

### Heat 的模版中的讲解

### 通过⼀个模版创建 OpenStack 的资源

### 更新⼀个模版

### 创建互相依赖 yaml 模版

## Lesson 10：Quiz

### 模拟题讲解

### 模拟题练习
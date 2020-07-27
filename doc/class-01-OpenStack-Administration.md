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

### Virtualization & OpenStack ( [Catalog](#catalog) )

1. 什么是虚拟化？虚拟化的发展历程如何？60-70 IBM / 80-90 VMWare / 2005-2010 Amazon / 2010 NASA Nebula & RackSpace Cloud Storage
1. 云计算的类型有几种类型？IaaS / PaaS / SaaS，只有 IaaS 是必须基于虚拟化的
1. OpenStack 的发展过程？模块化 & 服务化，核心项目 & 集成项目 => Big Tent

### OpenStack Infrastructure ( [Catalog](#catalog) )

1. OpenStack 哪些是核心项目？Keystone / Nova / Cinder / Neutron / Glance
1. [Design](https://docs.openstack.org/arch-design/design.html)

    ![](https://docs.openstack.org/arch-design/_images/osog_0001.png)

1. [Logical architecture](https://docs.openstack.org/install-guide/get-started-logical-architecture.html)

    ![](https://docs.openstack.org/install-guide/_images/openstack-arch-kilo-logical-v1.png)

1. [Conceptual architecture](https://docs.openstack.org/ocata/admin-guide/common/get-started-conceptual-architecture.html)

    ![](https://docs.openstack.org/ocata/admin-guide/_images/openstack_kilo_conceptual_arch.png)

### The Trend of Cloud Computing ( [Catalog](#catalog) )

1. 私有云、公有云、混合云的发展趋势如何？Azure / Aliyun / HW
1. IaaS & CaaS 谁会是未来的主流？
1. OpenStack 的发展趋势？

### OpenStack Reference ( [Catalog](#catalog) )

1. 官方文档在哪里？
1. 有哪些推荐的入门书？《每天五分钟玩转 OpenStack》，《OpenStack 设计与实现》

## Lesson 02：Keystone

### Keystone Concepts

1. 什么是 User / Group？有几种 Credentials / Authentication？用户名密码 / Token / API Key
1. 什么是 Project / Tenant / Account？
1. 什么是 Service / Endpoint？
1. 什么是 Role / Policy？

### Keystone Capablities

1. Keystone 怎么处理服务注册和服务发现？
1. Keystone 怎么处理组织和用户管理？用户、用户组、项目、配额
1. Keystone 怎么处理认证、鉴权和授权？角色、RBAC、Cloud Admin / Domain Admin

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

## Lesson 09：Heat

### Heat 的模版中的讲解

### 通过⼀个模版创建 OpenStack 的资源

### 更新⼀个模版

### 创建互相依赖 yaml 模版

## Lesson 10：Quiz

### 模拟题讲解

### 模拟题练习
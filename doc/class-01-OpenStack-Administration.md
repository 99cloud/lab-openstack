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
| | | | [OpenStack 基金会是怎么运作的？]() |
| | | | [OpenStack 的组件架构是怎样的？]() |
| | | | [OpenStack 的项目发展流程是怎样的？]() |
| | | | [如何与 OpenStack 社区交互？]() |
| | | | [云计算的技术发展趋势是怎样的？]() |
| | | [Lesson 02：管理身份认证服务 - Keystone](#) | [管理 OpenStack service catalog 和 endpoint](#) |
| | | | [创建 / 管理项⽬和租户]() |
| | | | [为 OpenStack 环境创建]()  |
| | | | [管理身份服务]() |
| | | | [管理配额]() |
| | 下午 | [Lesson 03：管理看板服务 - Horizon]() | [检验 Dashboard 的运⾏](#) |
| | | | [配置 Horizon 来⽀持多 Domain 登录](#) |
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

## Lesson 01：OpenStack Introduction - 介绍

### Virtualization & OpenStack

虚拟化和基于虚拟化技术的基础设施云计算技术

- 60 - 70 年代：IBM，虚拟化技术的开创者
- 80 - 90 年代：VMWare，X86 平台虚拟机技术的革命者
- 2005 年：Amazon，SOA（ Service-Oriented Architecture ），服务第一，EC2（ Elastic Compute Cloud ）
- 2010 年：OpenStack：NASA Nebula & RackSpace Cloud Storage

云计算的分类

- IaaS
- PaaS / FaaS
- SaaS

同行的产品

- CloudStack
- 桉树
- OpenNebula

### 了解 OpenStack 的⽬前的市场背景

### 理解构建云的组件

## Lesson 02：Keystone

### 管理 OpenStack service catalog 和 endpoint

### 创建 / 管理项⽬和租户

### 为 OpenStack 环境创建

### 管理身份服务

### 管理配额

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
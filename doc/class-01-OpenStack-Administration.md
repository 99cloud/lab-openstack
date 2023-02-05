# OpenStack-Administration

## Prefix

- 授课时长：
    - 上午：9:00 至 12:00
    - 下午：14:00 至 17:00
- Prerequisite
    - vim 基础操作 -- 编辑、修改、保存文件
    - 网络基础知识 -- 网段 cidr、vlan、vxlan、配置 linux 网卡等等
    - 基础的 linux 知识 -- 权限、文件系统、服务
    - systemd 的基础操作 -- 重启、关闭、启动、重载、查看 systemd 的服务

## Catalog

| Date | Time | Title | Content |
| ---- | ---- | ----- | ------- |
| 第 1 天 | 上午 | [1. 实验环境](#1-实验环境) | [实验环境介绍](#1-实验环境) |
| | | [2. OpenStack 概述](#2-openstack-概述) | [2.1 虚拟化与云计算](#21-虚拟化与云计算) |
| | | | [2.2 OpenStack 组件架构](#22-openstack-组件架构) |
| | | | [2.3 云计算的发展趋势](#23-云计算的发展趋势) |
| | | | [2.4 OpenStack 的通用概念](#24-openstack-的通用概念) |
| | | [3. 管理身份认证服务 - Keystone](#3-keystone) | [3.1 Keystone 模块概况](#31-keystone-模块概况) |
| | | | [3.2 Keystone 的基本概念有哪些？](#32-keystone-的基本概念有哪些) |
| | | | [3.3 Keystone 各功能的实现机理是怎样的？](#33-keystone-各功能的实现机理是怎样的) |
| | 下午 | [4. 管理看板服务 - Horizon](#4-horizon) | [4.1 Horizon 基本概念](#41-horizon-基本概念) |
| | | | [4.2 Horizon 基本功能](#42-horizon-基本功能) |
| | | | [4.3 通过 Horizon 创建一台虚拟机](#43-通过-horizon-创建一台虚拟机) |
| | | | [4.4 其它操作](#44-其它操作) |
| | | | [4.5 [可选] 新一代 Web 界面：Skyline](#45-可选-新一代-web-界面skyline) |
| | | [5. 管理计算服务 - Nova](#5-nova) | [5.1 理解虚拟化](#51-理解虚拟化) |
| | | | [5.2 介绍硬件加速虚拟化 KVM](#52-介绍硬件加速虚拟化-kvm) |
| | | | [5.3 Nova 基本概念](#53-nova-基本概念) |
| | | | [5.4 Nova 的基本功能](#54-nova-的基本功能) |
| | | | [5.5 Nova 小结](#55-nova-小结) |
| 第 2 天 | 上午 |  [6. 管理镜像服务 - Glance](#6-glance) | [6.1 理解 OpenStack 中使⽤的镜像](#61-理解-openstack-中使的镜像) |
| | | | [6.2 Glance 基本概念](#62-glance-基本概念) |
| | | | [6.3 Glance 小结](#63-glance-小结) |
| | | | [6.4 Glance 基本功能](#64-glance-基本功能) |
| | | [7. 管理块存储 - Cinder](#7-cinder) | [7.1 理解 Cinder 的作⽤](#71-理解-cinder-的作) |
| | | | [7.2 Cinder 基本概念](#72-cinder-基本概念) |
| | | | [7.3 统⼀的存储解决⽅案 Ceph 的简介](#73-统的存储解决案-ceph-的简介) |
| | | | [7.4 管理卷](#74-管理卷) |
| | | | [7.5 Cinder 基本功能](#75-cinder-基本功能) |
| | | | [7.6 Cinder 小结](#76-cinder-小结) |
| | | | [7.7 备份与快照的差别](#77-备份与快照的差别) |
| | 下午 | [8. 管理⽹络服务 - Neutron](#8-neutron) | [8.1 理解 Neutron 的作⽤](#81-理解-neutron-的作) |
| | | | [8.2 网络概念](#82-网络概念) |
| | | | [8.3 Neutron 基本概念](#83-neutron-基本概念) |
| | | | [8.4 ⽣产环境中的实施⽅案](#84-产环境中的实施案) |
| | | | [8.5 理解节点的内部⽹络的实现](#85-理解节点的内部络的实现) |
| | | | [8.6 [可选] Distributed Virtual Router](#86-可选-distributed-virtual-router) |
| | | | [8.7 [可选] ⽹络加速的技术 dpdk、sr-iov、TSN 的介绍](#87-可选-络加速的技术-dpdksr-iovtsn-的介绍) |
| | | | [8.8 Neutron 基本功能](#88-neutron-基本功能) |
| | | | [8.9 管理安全组规则](#89-管理安全组规则) |
| 第 3 天 | 上午 | [9. Devstack 服务的管理](#9-devstack-服务的管理) | [9.1 理解 Devstack 的作⽤](#91-理解-devstack-的作) |
| | | | [9.2 Devstack 基本概念](#92-Devstack-基本概念) |
| | | | [9.3 Devstack 基本功能](#93-Devstack-基本功能) |
| | | | [9.4 Debug](#94-debug) |
| | | [10. Swift](#10-swift) | [10.1 理解 Swift 的使⽤场景](#101-理解-swift-的使场景) |
| | | | [10.2 Swift 基本概念](#102-swift-基本概念) |
| | | | [10.3 Swift 基本功能](#103-swift-基本功能) |
| | | | [10.4 [可选] 管理到期的对象](#104-可选-管理到期的对象) |
| | | [11. 编排服务 - Heat](#11-heat) | [11.1 Heat 的模版中的讲解](#111-heat-的模版中的讲解) |
| | | | [11.2 Heat 基本概念](#112-heat-基本概念) |
| | | | [11.3 Heat 基本功能](#113-heat-基本功能) |
| | | | [11.4 其它](#114-其它) |
| | 下午 | [12. Quiz](#12-quiz) | [模拟题讲解](#模拟题讲解) |
| | | | [模拟题练习](#模拟题练习) |

## 1. 实验环境

[Catalog](#catalog)

- [实验环境访问方式](/src/ansible-cloudlab-centos/README.md)
- [可选] [如何自己动手搭建 DevStack 实验环境？](devstack-aio.md)

## 2. OpenStack 概述

[Catalog](#catalog)

1. 云计算分为 IaaS / CaaS / SaaS 三种，其中 IaaS 云计算是主流，我们在课程中只讨论 IaaS 云计算
1. 以 AWS 为代表的 IaaS 云计算是一种基于**虚拟化**技术的**自助式**服务平台，其它云计算厂商均以 AWS 为模版

### 2.1 虚拟化与云计算

[Catalog](#catalog)

1. 什么是虚拟化？

    虚拟化是云计算的基础。简单地说，**虚拟化使得在一台物理服务器上可以跑多台虚拟机**。虚拟化的目的：**1. 资源隔离，2. 资源限制**

    - 虚拟化共享物理机的 CPU、内存、IO 硬件资源，但逻辑上虚拟机之间是相互隔离的
    - 物理机我们一般称为宿主机（Host），宿主机上面的虚拟机称为客户机（Guest）

    Hypervisor 程序将 Host 的硬件虚拟化，并提供给 Guest 使用，分为：全虚拟化（一型虚拟化）和半虚拟化（二型虚拟化）。

    - **全虚拟化 Hypervisor 是一个特殊定制的 Linux 系统**，直接安装在物理机上。比如 Xen 和 VMWare 的 EXSi。全虚拟化一般对硬件虚拟化功能做了特别优化，性能更好。
    - 半虚拟化先安装标准操作系统，Hypervisor 作为 OS 上的一个程序模块运行，并对虚拟机进行管理。比如 KVM，VirtualBox，VMWare WorkStation，VMWare Player，VMWare Fusion 等。半虚拟化基于普通操作系统，比较灵活，比如支持虚拟机嵌套（在 KVM 虚拟机中再运行 KVM）。

1. 虚拟化的发展历程如何？

    - 60-70 IBM
    - 80-90 **VMWare**
    - 2005-2010 Amazon
    - 2010 NASA Nebula & RackSpace Cloud Storage
1. 计算的发展历经了哪些阶段？
    - 大型机：集中式计算
    - 个人 PC：分布式计算
    - 移动互联网 + 云计算：泛在计算
1. 云计算的类型有几种类型？
    - IaaS / PaaS / SaaS
    - 只有 IaaS 是必须基于虚拟化的

        ![iaas](/img/iaas.png)

1. 云计算发展历程是怎样的？
    - 最初的概念是”网络即是电脑”
    - 尔后 Amazon 推出的弹性云计算 (EC2) 提供用户使用资源并且收费，大致奠定了云计算的商业用途。**阿里云**、OpenStack 都是 Amazon Web Services (AWS) 的追随者。
    - OpenStack 是一个开源的云平台，它属于云计算当中我们常说的 IaaS（infrastructure as a service）。**OpenStack 是一个云管理操作系统，用来控制数据中心中的计算、存储、网络资源池**，管理员通过 API / CLI 和 Web 界面为用户提供所需的资源。

1. KVM 基础

    KVM（Kernel-Based Virtual Machine）是 x86 平台上应用最广泛的虚拟化方案。AWS / 阿里云都从最初的 XEN 转向了 KVM；OpenStack 对 KVM 支持得也最好。

    **KVM 内核模块叫 kvm.ko，只用于管理 VM 的 CPU 和内存。IO 虚拟化由 Linux 内核和 QEMU 来实现**。

    Libvirt 是 KVM 的管理工具，除了能管理 KVM，还能管理 XEN、VirtualBox 等。OpenStack 底层通过 Libvirt 来简介管理 KVM。**Libvirt 包含：后台 Daemon 程序 libvirtd、API（virt-manager 就是基于 libvirt API 开发）和命令行工具 virsh**。可以通过 virt-manager 对虚拟机进行创建、删除、开关机、快照等管理操作，也可以通过 virsh 命令行管理，比如：`virsh list --all`。

    - virt-manager 可以选 import exist disk image，通过 cirros（特制很小的 linux 镜像）启动（<http://download.cirros-cloud.net>），KVM 默认在 `/var/lib/libvirt/images` 位置查找。100 M，1 Core 就可以运行了。
    - virt-manager 也可以从 iso 安装 Guest OS
    - virt-manager 也可以通过 File / Add Connection 连接远程 Host 主机上的 Guest VM。远程宿主机上的 libvirt 需要允许远程管理。

        ```conf
        以 ubuntu 14.04 为例

        # /etc/default/libvirt-bin
        start_libvirtd="yes"
        libvirtd_opts="-d -l"

        # /etc/libvirt/libvirtd.conf
        listen_tls = 0
        listen_tcp = 1
        unix_sock_group = "libvirtd"
        unix_sock_ro_perms = "0777"
        unix_sock_rw_perms = "0770"
        auth_unix_rw = "none"
        auth_tcp = "none"
        ```

        然后重启 libvirtd：`service libvirt-bin restart`

1. 计算虚拟化：CPU 和内存

    现在用到的 Intel 和 AMD CPU 都支持 VT 硬件虚拟化了，可以用 `egrep -o '(vmx|svm)' /proc/cpuio` 命令检查确认。**一个 KVM VM 在 Host 上其实是一个 qemu-kvm 进程，VM 中的每一个 vCPU 则对应 qemu-kvm 进程中的一个线程**。因此，vCPU 的总量可以超过物理 CPU 的总量，这叫做 CPU 超配（overcommit）。超配使得 VM 可以充分使用 Host 的 CPU 资源，前提是在同一时刻，不是所有的 VM 都 CPU 满负荷运行。

    KVM 需要完成 VA（虚拟内存）-> PA（物理内存）-> MA（机器内存）之间的地址转换。其中，Guest OS 完成 VA -> PA，KVM 完成 PA -> MA。内存也可以 overcommit，但是要小心测试和实时监控，避免 OOM（Out of Memory，内存溢出）。

1. 存储虚拟化

    KVM 的存储虚拟化是通过存储池（Storage Pool）和卷（Volume）来管理的。Storage Pool 是 Host 上可以看到的一片存储空间。Volume 是在 Storage Pool 中划分出的一块空间，Host 将 Volume 分配给主机，在 VM 中看到的就是一块硬盘。Storage Pool 可以是多种类型：目录，LVM，iSCSI（使原来用于本机的 SCSI 协议可以通过 TCP/IP 扩展，方便存储集成、灾难恢复），Ceph，参考：<http://libvirt.org/storage.html>

    - 文件目录类型的 Storage Pool

        **KVM 将 Host 的 `/var/lib/libvirt/images/` 作为默认的 Storage Pool。其中的一个文件就是一个 Volume**。

        KVM 所有可使用的 Storage Pool 都定义在 Host 的 `/etc/libvirt/storage` 目录下，每一个 Pool 对应一个 xml 文件，默认有一个 default.xml。

        ```console
        [root@lab-c2009 storage]# pwd
        /etc/libvirt/storage

        [root@lab-c2009 storage]# ls
        autostart  default.xml  images.xml
        ```

        ```xml
        [root@lab-c2009 storage]# cat default.xml
        <!--
        WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
        OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
        virsh pool-edit default
        or other application using the libvirt API.
        -->

        <pool type='dir'>
        <name>default</name>
        <uuid>06a9233b-c82b-4232-b65c-019f217b6383</uuid>
        <capacity unit='bytes'>0</capacity>
        <allocation unit='bytes'>0</allocation>
        <available unit='bytes'>0</available>
        <source>
        </source>
        <target>
            <path>/var/lib/libvirt/images</path>
        </target>
        </pool>
        ```

        可以看到 pool type 是目录，路径是 `/var/lib/libvirt/images`

        ```console
        [root@lab-c2009 storage]# ls /var/lib/libvirt/images/
        lab-c2009-devstack-aio.qcow2
        ```

        使用文件做 Volume 有很多优点：**存储方便、移植性好、可复制、可远程访问**。可远程访问的意思是 Volume 文件可以存储在 NFS 或者分布式文件系统 GlusterFS，这样**镜像文件就可以在多个 Host 之间共享，便于 VM 在不同宿主机之间 Live Migration。如果是分布式文件系统，多副本的特性还可以保证镜像文件的高可用**。

        KVM 支持多种 Volume 文件格式：

        - raw 是默认格式，即原始磁盘格式，移植性好，性能好，但大小固定，不能节省磁盘空间。**如果是 Ceph 作为存储后端，应该用 raw 格式，因为用 qcow2 也不会节省空间，反而会影响性能**
        - qcow2 是推荐格式，cow 表示 copy on write，能够节省磁盘空间，支持 AES 加密，支持 zlib 压缩，支持多快照。
        - vmdk 是 VMWare 的虚拟磁盘格式，因此 VMWare 虚拟机可以直接在 KVM 上运行。

    - [可选] LVM 类型的 Storage Pool

        Host 上的 VG（Volume Group）中的 LV（Logic Volume） 也可以作为虚拟磁盘分配给 VM 使用，但 **LV 没有磁盘的 MBR 引导记录，不能作为虚拟机的启动盘，只能作为数据盘使用**。这种配置下，VG 就是 Storage Pool，LV 就是 Volume。

        LV 的优点是性能较好，缺点是管理和移动性方面不如镜像文件，而且不能通过网络远程使用。

1. 网络虚拟化

    网络虚拟化是虚拟化技术中最复杂的部分，下图是[计算节点（可以理解为 KVM 宿主机）虚拟网络的逻辑图](references/Neutron-Network-Namespaces-and-IPtables-Technical-deep-dive.pdf)。

    ![](/img/network-virtualization-on-compute-node.png)

    Host 有一块连接外网的 eth0，上面跑了 1 个 虚拟机 VM1，如何能让 VM1 访问外网？

    - 将物理网卡 eth0 直接分配给 VM1。这样 Host 和其它 VM2 就没有网卡，无法访问外网了。
    - 给 VM1 分配一个虚拟网卡 vnet0，通过 Linux Bridge（简单理解为二层交换机） br0 将 eth0 和 vnet0 连接起来。

        ![](/img/linux-bridge.png)

        br0 会将 eth0/vnet0/vnet1 数据转发分享，使得 VM1 和 VM2 可以彼此通信，也能透过 eth0 与外部网络通信。

    - virbr0 是 KVM 默认创建的一个 Bridge，其作用是为连接其上的虚拟网卡提供 NAT 访问外网的功能。参考：<https://wiki.libvirt.org/page/VirtualNetworking>。这个和 br0 不一样，在 br0 的情况下，VM1 通过自己的 IP 直接与外网通信，不会经过 NAT 地址转换。

        ![](/img/Host_with_a_virtual_network_switch_in_nat_mode_and_two_guests.png)

    - Linux Bridge + VLAN

        ![](/img/linux-bridge-vlan.png)

        **eth0 相当于 Trunk 口，vnet0 / brvlan10 / eth0.10 都是 vlan10 的 Access 口**。Access 口（网卡和交换机之间）只能属于一个 VLAN，数据包流入 Access 口后，会被打上所在 VLAN 的标签。数据包在通过 Trunk 口（交换机和交换机之间）时，始终带着自己的 VLAN 标签。

### 2.2 OpenStack 组件架构

[Catalog](#catalog)

1. OpenStack 的核心项目有哪些？Keystone / Nova / Glance / Neutron / Cinder

    ![simpleOpenstackArch](/img/simpleOpenstackArch.png)

1. [设计原理图](https://docs.openstack.org/arch-design/design.html)

    ![](https://docs.openstack.org/arch-design/_images/osog_0001.png)

1. [逻辑架构图](https://docs.openstack.org/install-guide/get-started-logical-architecture.html)

    ![](/img/openstack-arch-kilo-logical-v1.png)

1. [概念架构图](https://docs.openstack.org/ocata/admin-guide/common/get-started-conceptual-architecture.html)

    ![](https://docs.openstack.org/ocata/admin-guide/_images/openstack_kilo_conceptual_arch.png)

1. OpenStack 的发展过程？模块化 & 服务化，核心项目 & 集成项目 => Big Tent
1. 平均 6 个月版本更新，每个版本维护 18 个月，bugfix
1. [OpenStack 组件官网](https://www.openstack.org/software/project-navigator/openstack-components#openstack-services)
1. [Stackalytics](https://www.stackalytics.io/)
1. [Source code](https://opendev.org/openstack)
1. [Launchpad](https://bugs.launchpad.net/)
1. [Review](https://review.opendev.org/)

    ![](/img/qualityfordevelop.png)

### 2.3 云计算的发展趋势

[Catalog](#catalog)

1. 私有云、公有云、混合云的发展趋势如何？AWS / Azure / Aliyun / Huawei
1. IaaS & CaaS 谁会是未来的主流？
    - VM、容器、裸机的编排需求长期共存
    - OpenStack 擅长 VM & 裸机编排，以及存储和网络虚拟化。在容器化方面，Magnum 和 Kata 短时间内都看不到成为主流的趋势
    - K8S 擅长容器编排，通过插件支持 VM 编排和网络多平面，但仍显稚嫩
1. OpenStack 的优势和发展趋势？
    - Ironic 裸机云的加强
    - 容器化部署和运维：kolla-ansible & openstack-helm
    - 软件定义存储：SDS -- Ceph and Cinder-volume，高性能 高可用性 高可扩展性 支持三种存储接口(文件，块，对象)
    - 软件定义网络：SDN -- Neutron Server，控制转发分离 集中控制 虚拟化

### 2.4 OpenStack 的通用概念

[Catalog](#catalog)

1. 官方文档在哪里？
1. 有哪些推荐的入门书？《每天五分钟玩转 OpenStack》，《OpenStack 设计与实现》

#### 2.4.1 OpenStack 模块间和模块内如何通信？

1. infra: restful api
1. inner: message queue

![](/img/communication.png)

#### 2.4.2 什么是 Restful API？

OpenStack 是由很多个核心组件组合而成，每个组件都负责他们自己的一小块的功能比如负责提供计算服务的是Nova，提供网络服务的是 Neutron，他们各自都有属于自己的管理接口，所谓管理接口就是一个基于 http 请求的一个 Web 服务，主要是用于接受命令行工具或者组件的 http 请求。访问管理接口的过程，使用者发出请求 (request) 以 RESTful 的风格,基于 http 网络协议，传送送到处理RESTful 封包的接口，又称 REST API，完成对数据库的增删查找.

![](/img/restfulapi.png)

#### 2.4.3 什么是消息队列？

![](/img/rabbitmqex.png)

![](/img/rabbitmqex2.png)

![](/img/rabbitmqex3.png)

#### 2.4.4 Openstack 如何处理消息？slo.messageing

1. Event Notification
    - 将讯息发送到总线上面，对此类讯息感兴趣的服务进程会去获取此讯息，做进一步的处理
    - 举例来说: 计量服务的 Ceilometer 就是监听总线获取其他服务的事件，进而实现计量与监控
1. Remote Procedure Call(RPC)
    - Cast: 异步执行远程方法,调用者不会等待结果返回
    - Call: 同步执行远程方法,调用者会等待结果返回

    ![](/img/oslo.png)

#### 2.4.5 数据库和对象关系模块：sqlachemy

Openstack 以 Python 语法实现 IaaS 架构，在各组件调度资源的过程，需要一数据库记录所有平台管理资料底层后台数据库琳琅满目 MySQL Mariadb PostgreSQL Sqlite3 等上层开发需要使用 Python 语法实现，基于这样环境 Openstack 使用 SQLAchemy 来管理数据库，SQLAchemy 是一个以 Python 语法写成向下对数据库键值进行修改的工具

![](/img/sqlachemy.png)

## 3. Keystone

[Catalog](#catalog)

### 3.1 Keystone 模块概况

[Catalog](#catalog)

1. Keystone 在 OpenStack 中起什么作用？
    - **用户、租户和权限管理**
    - **认证**：用户的身份认证服务包括组件和组件之间的身份认证
    - **鉴权**：提供 RBAC（Role Based Access Control） 权限体系
    - **服务注册和服务发现**：为 OpenStack 提供目录服务，维护 OpenStack Services 的 Endpoint
1. 参考官方文件
    - <https://docs.openstack.org/keystone/latest/>

### 3.2 Keystone 的基本概念有哪些？

[Catalog](#catalog)

Keystone 的核心概念包括：

- User（用户）
- Role（角色）
- Credential（凭证）
- Authentication（认证）
- Endpoint（端点）
- Service（服务）
- Project / Tenant（项目/租户）
- Token（令牌）
- ...

逐一来看：

1. User 指使用 OpenStack 的实体，可以是真正的用户（用户 peter），其它系统（云管管理系统 CMP 等）或者服务（OpenStack 为 nova/cinder 等服务创建了相应的 User 作为服务账号）。

    当 User 请求访问 OpenStack 时，Keystone 会对其进行身份认证和鉴权。

    Horizon 在 Identity -> Users 中可以管理用户。

1. Credentials 是 User 用来证明自己身份的信息，可以是：
    - 用户名 / 密码
    - Token
    - API Key
    - 其它高级方式
1. Authentication 是 Keystone 验证 User 身份的过程。比如，User 访问 OpenStack 时向 Keystone 提交用户和密码形式的 Credentials，Keystone 验证通过后会给 User 签发一个 Token 作为后续访问用的 Credentials。
1. Token 是由数字和字母组成的字符串，User 成功 Authentication 后，由 Keystone 分配给 User。
    - Token 用作访问 Service 的 Credential
    - Service 会通过 Keystone 验证 Token 的有效性
    - Token 的有效期默认是 24 小时，这个时长可以在 Keystone 配置文件中设置

    发放与使用流程：

    - Client obtains token from the Keystone (by user password)
    - Client sends request to Nova API to launch VM instance
    - Nova API verifies token in Keystone
    - Nova requests Keystone to get all available quotas for project/user. Nova calculates amount of used resources and allows or permits operation
    - Nova API calls nova-compute via RPC to launch VM instance.

    ![](/img/token.png)

1. Project / Tenant 就是项目（租户），用于将 OpenStack 资源（计算、存储、网络）进行分组和隔离。
    - 资源的所有权属于 Project 而不是 User
    - 在 OpenStack 中，Tenant / Project / Account 术语通用，最常用的是 Project
    - 每个 User（包括 admin）必须以某个权限绑定到 Project 里才能访问该 Project 的资源。一个 User 可以以不同权限绑定到多个 Project。一个 Project 也可以以不同权限被多个用户绑定。
    - admin 相当于 root 用户，具有 Project 中的最高权限。

    在 Horizon 中，我们通过 Manage Members 将用户绑定到 Project 中。
1. Group 组顾名思义就是一个 User 的集合，一般我们会把一个用户关联到一个项目中，每次关联的时候都要设置一个角色比较麻烦，有了组以后我们可以把组加到租户当中去并关联一个角色，以后所以加入到这个组当中的用户就继承了这个组在这个租户当中的角色
1. 什么是 Domain: 在 OpenStack 当中域是用来实现真正的多项目/租户模式的一种方法，在没有域出现之前 OpenStack 有着一个权限的场景，当你把一个用户任何一个项目/租户当中去的时候，你如果关联的是  admin 的角色的话，这个时候这个用户突然就成为了 OpenStack 超级管理员，这并非我们所希望的场景，使用了域以后我们就可以实现真正意义上的多项目/租户模式了，把一个用户加到 default 以外的域中的项目并关联到 admin 的时候，这个用户就不再是整个 OpenStack 的管理员了，他只能管理这个域下面的所有的项目/租户，当然你要开启多项目/租户模式你得替换掉 /etc/keystone/policy.json 文件来开启

    ![](/img/DomainUserProjectRole.png)

1. 什么是服务终端 service endpoint？
    - 服务终点即一个服务提供的地址比如 http://192.168.100.20:5000/v3，这就是一个服务终点，服务终点是用来提供基于 http 请求的 API 方法的一个地址
1. 什么是目录服务？
    - 之前提到 OpenStack 有很多个核心组件组合而成的，每个组件都有一个或多个管理接口，每个管理接口提供服务都是以 web 服务的形式出现的，那么他们都有一个服务的终点地址比如 keystone 的(http://ip:5000/v3)，我们怎么才能找到每个组件的终端呢？因为这些服务可以很方便的迁移到任何网络可达的物理服务器上，所有这里我们要一个机制来集中管理服务的终点，就像服务终点的路由器一样
1. 什么是 Role / Policy？
    - keystone 遇到不同的使用者做出不同请求的问题 ( 例如: 创建虚拟机 删除云盘 ) 要透过 role 跟 policy 协作来满足需求，每一个调度请求都会有一个对应的 policy 里面存有多向属性，其中一个就是 role。 再来，每个被创建的使用者都会被绑定一个 role (admin / member)，当使用者发出请求调度服务的时后，keystone 收到后会确认这个服务的 policy role 是不是这个使用者可以有权利访问的，如果有才可以继续，反之拒绝

    ![](/img/api3flow.png)

### 3.3 Keystone 各功能的实现机理是怎样的？

[Catalog](#catalog)

1. Keystone 怎么处理服务注册和服务发现？
    - 练习: 如何添加一个新的服务终端?
    - 我们为 OpenStack 写了一个新的服务，并且已经和开发团队约定好我们的服务以 Rest API 的方式部署，我们的服务名称叫 myService，我们的服务终端的地址为 http://172.25.0.10:3838。

    ```bash
    openstack service create --name myService --description "helloworld" myService

    openstack endpoint create --region RegionOne myService public http://172.25.0.10:3838
    openstack endpoint create --region RegionOne myService internal http://172.25.0.10:3838
    openstack endpoint create --region RegionOne myService admin http://172.25.0.10:3838
    ```

    注意，**这里 `--region` 后面只能写 `RegionOne`**，RegionOne 是在部署当前 OpenStack 环境，创建基础服务 endpoint 时就默认填写的。

    注意，创建完 endpoint 后，只有 public 类型的 endpoint 会在 Horizon 界面上可以看到。但 **Horizon 界面有缓存，需要切换项目，或者退出重新登录**，才能显示出来。

    ![](/img/horizon-endpoint-list.png)

1. Keystone 怎么处理组织和用户管理？用户、在项目中绑定角色

    ```bash
    # 创建一个用户
    openstack user create --password johnpassword john

    # 更新一个用户
    openstack user set --password newpassword john

    # 用户列表
    openstack user list

    # 查看详细
    openstack user show john

    # 将用户关联到项目/租户
    openstack role add --user john --project demo member

    # 删除一个用户
    openstack user delete john
    ```

1. Keystone 怎么处理认证、鉴权和授权？角色、RBAC、Cloud Admin / Domain Admin

    练习: 只允许 admin 创建云盘

    参考 <https://docs.openstack.org/cinder/latest//configuration/block-storage/samples/policy.yaml.html>，默认的 policy 文件在 /etc/cinder/policy.yaml。也可以在 cinder.conf 文件的 `[oslo_policy]` 块 `policy_file` 配置项指定 policy 文件路径。

    ```bash
    # 检查 /etc/cinder/ 路径下面有无 policy 文件，如果没有就新增一个
    oslopolicy-sample-generator --namespace cinder --output-file policy.yaml
    sudo cp policy.yaml /etc/cinder/policy.yaml
    ```

    ```yamml
    # 修改 policy rule 权限
    "context_is_admin": "role:admin"
    "volume:create": "rule:context_is_admin"
    ```

    ```bash
    # 重启服务
    systemctl restart devstack@c-api
    ```

    此时，在 demo 项目中 member 角色的 john 就无法创建云硬盘（卷 volume）了，创建时会返回 403，说 volume:create 不被允许。只有对应 project 下 admin 权限的用户可以创建卷。

    如果删除 `/etc/cinder/policy.yaml` 文件，然后重启 cinder api 服务，那么 member 角色会恢复可以创建卷的能力。可以自己试一下

    ```bash
    rm -rf /etc/cinder/policy.yaml
    systemctl restart devstack@c-api
    ```

    *在 Victoria 版本中依然可以使用 json 格式的 policy 文件，参考 <https://docs.openstack.org/oslo.policy/victoria/cli/oslopolicy-policy-generator.html>，所以上述命令在 Victoria 版本中没有问题。但是 [wallaby](https://docs.openstack.org/oslo.policy/wallaby/cli/oslopolicy-policy-generator.html) 以后，policy 格式被废弃，不再有 format 参数，默认就是 yaml 格式，参考：<https://docs.openstack.org/oslo.policy/latest/cli/oslopolicy-policy-generator.html>。*

    ```bash
    # 检查 /etc/cinder/ 路径下面有无 policy 文件，如果没有就新增一个
    oslopolicy-sample-generator --namespace cinder --format json --output-file policy.json
    sudo cp policy.json /etc/cinder/policy.json
    ```

    添加或是修改 policy 路径到 cinder.conf

    ```ini
    [oslo_policy]
    policy_file = /etc/cinder/policy.json
    ```
    
    修改 policy rule 权限
    
    ```yaml
    "context_is_admin": "role:admin"
    "volume:create": "rule:context_is_admin"
    ```

    ```bash
    # 重启服务
    systemctl restart devstack@c-api
    ```

## 4. Horizon

[Catalog](#catalog)

### 4.1 Horizon 基本概念

[Catalog](#catalog)

Horizon 为 OpenStack 提供了界面管理服务，让 OpenStack 管理员和用户都能来通过界面的方式来管理 OpenStack，而不是纯粹的命令行管理，因为一般用户很难接受使用命令行的方式来使用和管理他们在 OpenStack 中创建的资源

一般 Horizon 会安装在 OpenStack 的控制器上面，我们只需要打开浏览器输入 http://controllerip/dashboard 即可访问你的的 Horizon 的界面。

### 4.2 Horizon 基本功能

[Catalog](#catalog)

- Django 是 python 的开源的做 web 技术，基于mvc框架 (model、view、controller) 的 web framework。
- AngulaJS 前端 javascript 脚本，是谷歌研发的，为了在浏览器端来提高用户互动体验的一套 javascript 框架。

- 检验 Dashboard 的运⾏
- [可选] 配置 Horizon 来⽀持多 Domain 登录

### 4.3 通过 Horizon 创建一台虚拟机

[Catalog](#catalog)

- 管理 flavor
- 管理 Nova ⽤户密钥对（ keypair ）
- 管理网络
- 管理项⽬的安全组规则
- 分配安全组规则给实例
- 理解虚拟机从镜像启动和从云盘启动的区别
- 启动⼀个新实例

    ![](/img/horizon-createvm-01-launch.png)

    ![](/img/horizon-createvm-02-name.png)

    ![](/img/horizon-createvm-03-image.png)

    ![](/img/horizon-createvm-04-image-selected.png)

    ![](/img/horizon-createvm-05-flavor.png)

    ![](/img/horizon-createvm-06-flavor-selected.png)

    ![](/img/horizon-createvm-07-network.png)

    创建好 VM 之后，可以访问其 web console

    ![](/img/horizon-vm-01-detail.png)

    ![](/img/horizon-vm-02-console.png)

    ![](/img/horizon-vm-03-novnc.png)

- 分配 floating IP 给实例
- 从实例上分离 floating IP

### 4.4 其它操作

[Catalog](#catalog)

- 管理 compute instance（ 如启动、关闭、终⽌ ）
- nova 管理虚拟机的静态数据的位置

    ```console
    $ vi /etc/nova/nova.conf

        ...
        instances_path = /opt/stack/data/nova/instances
        state_path = /opt/stack/data/nova
    ```

### 4.5 [可选] 新一代 Web 界面：Skyline

[Catalog](#catalog)

参考：<https://opendev.org/openstack/skyline-apiserver>

## 5. Nova

[Catalog](#catalog)

### 5.1 理解虚拟化

[Catalog](#catalog)

1. 对物理资源进行池化，允许单个物理硬件创建多个模拟环境或专用资源
1. 是什么实现了虚拟化? Hypervisor
1. Hypervisor 是什么? a piece of software or driver which run on the physical device
1. Hypervisor function
    - 将物理资源池化
    - 分配资源给虚拟机
    - 管理虚拟机生命周期
1. 虚拟化的类型
    - Type1: installed directly on top of physical，named as bare metal hypervisors (ex: VMware ESXi，Microsoft Hyper-V，KVM)
    - Type2: installed on Host OS which sits between physical server and hypervisor，named as hosted hypervisors(VMware Workstation，VirtualBox)

    ![](/img/virtual1.png)

### 5.2 介绍硬件加速虚拟化 KVM

[Catalog](#catalog)

- kvm: kernel virtual machine 他属于硬件加速的虚拟化，他依赖于 cpu 的虚拟化功能 intel-vt 或者 amd-v 等技术，可以对 NUMA 的框架的 CPU 做定制的调优
- qemu-kvm: 帮助 kvm 进行 io 模拟的虚拟机监控器，主要负责模拟 io(input/output)

    ![](/img/virtual2.png)

    ![](/img/virtual3.png)

    ![](/img/virtual4.png)

### 5.3 Nova 基本概念

[Catalog](#catalog)

1. 我们回到 nova，之前提到 openstack 使用的 hypervisor 是用 kvm，除此之外还可以支持其他的 hypervisor 比如 virtual box、vmware、xen、qemu 当我们的计算的节点的 cpu 不支持硬件加速的时候我们可以使用 qemu 来代替

    ![](/img/virtual5.png)

1. 虚拟机属性？
    - User:
    - region: 物理地域的区分，比如我们在大连部署了一套 openstack 另外在上海部署了另外一套 openstack，他们的除了管理界面和keystone是共享的其他的资源都是独立
    - available zone: 可用区域是对用户可见，比如我们使用阿里云的时候我们会去选需要哪个机房的服务器，openstack 预设的可用域是 nova
    - host aggregation: 我们把一组比较有特性的计算节点归类到一个分组中我们叫做 host aggregation，比如把 I7 cpu 的计算节点归类到一个 host aggregation 中，结合 flavor 这个 host aggregation 下的计算节点只有特定租户下的用户才可以在上面启动虚拟机，host aggregation 用户是不可见的，是管理员来设置的，他会影响 nova scheduler 的算法
    - flavor: 预建的虚拟机配置的列表。
    - Host Group: 集群标签虚拟机，可选择亲和或是反亲和，来决定在哪台宿主机孵化
1. host aggregation 示例:
    - AggregateCoreFilter: 针对HostAggregate设置一个metadata(Key，Value)，比如设置cpu_allocation_ratio=10，超过则该宿主机被过滤
    - SameHostFilter: 在指定虚拟机所在主机上分配虚拟机

        ![](/img/virtual6.png)

1. nova 核心组件
    - nova-api: 和其他核心项目组件一样都一个管理接口
    - nova-scheduler: 将虚拟机分配到具体的计算节点的服务
    - nova-conductor: 负责虚拟机的监控与分配整逻辑实现
    - nova-compute: 运行在计算节点上的服务，负责调度 libvirt 启动虚拟机的服务
    - RabbitMQ: 是世界上比较主流的消息队列被广泛使用

    ![](/img/virtual7.png)

    ![](/img/virtual8.png)

### 5.4 Nova 的基本功能

[Catalog](#catalog)

1. nova 计算资源池的划分方式

    ```console
    # 首先创建一个 host aggregation 叫 vip_host_aggr 做并创建一个 available zone 叫做 demo
    $ nova aggregate-create [vip_host_aggr] [vip_zone]

    # 创建一个 host aggregation 叫 regular_host_aggr 并将它加入到 available zone vip_zone 和 regular_zone 中，程序会自动判断是新建 az 还是关联现有 az
    $ nova aggregate-create [regular_host_aggr] [regular_zone]

    # 将计算节点加入到各自的 host aggregation 中去
    $ nova aggregate-add-host [vip_host_aggr] [I7_compute_node]
    $ nova aggregate-add-host [regular_host_aggr] [I5_compute_node]

    # 为 vip_host_aggr 设置特殊的属性来和 flavor 产生关联
    $ nova aggregate-set-metadata [vip_host_aggr] [ForVip=true]
    $ nova aggregate-set-metadata [regular_host_aggr] [ForRegular=true]

    # 为了 vip 租户创建一个 flavor
    $ openstack flavor create --private-ram 256 --disk 1 --vcpus 4 m1.flavor_vip
    $ nova flavor-access-add [m1.flavor_vip] [project_vip]
    $ nova flavor-key m1.flavor_vip set ForVip=true

    # 到此，完成 vip i7 调度的关联创建，接下来说明如何使用
    $ source project_vip_userrc
    $ openstack server create --flavor m1.flavor_vip ……
    ```

1. nova cloud-init 服务
    - 当虚拟机在 OpenStack 启动过的时候，一些信息比如 SSH key、语言设置、主机名都是放在 nova 的 metadata 服务中的，这样可以方便虚拟机的迁移
    - linux 安装 cloud-init daemon: 我们使用的镜像中预装的软件，为了执行预启动的脚本

    ```console
    # 举例: 创建使用者
    $ cat > create_user.yaml << EOF

        #cloud-config
        groups:
          - ubuntu: [root,sys]
          - cloud-users
        users:
          - default
          - name: foobar
            gecos: Foo B. Bar
            primary_group: foobar
            groups: users
            selinux_user: staff_u
            expiredate: '2032-09-01'
            ssh_import_id: foobar
            lock_passwd: false
            passwd: $6$j212wezy$7H/1LT4f9/N3wpgNunhsIqtMj62OKiS3nyNwuizouQc3u7MbYCarYeAHWYPYb2FT.lbioDm2RrkJPb9BZMN1O/
      - name: barfoo
            gecos: Bar B. Foo
            sudo: ALL=(ALL) NOPASSWD:ALL
            groups: users, admin
            ssh_import_id: None
            lock_passwd: true
            ssh_authorized_keys:
              - <ssh pub key 1>
              - <ssh pub key 2>
          - name: cloudy
            gecos: Magic Cloud App Daemon User
            inactive: '5'
            system: true
          - name: fizzbuzz
            sudo: False
            ssh_authorized_keys:
              - <ssh pub key 1>
              - <ssh pub key 2>
          - snapuser: joe@joeuser.io
          - name: nosshlogins
            ssh_redirect_user: true
        EOF
    ```

    ![](/img/cloudinit.png)

1. nova 创建虚拟机

    ```console
    $ openstack server create --image [cirros] --flavor [m1.mysmall] --security-group [default] --key-name [mykey] --nic net-id=[network_id] [instance1]
    # 为虚拟机绑定 floating ip
    $ openstack floating ip create [public]
    $ openstack server add floating ip [instance1] [172.25.0.232]
    $ openstack server stop [instance1]
    ```

### 5.5 Nova 小结

[Catalog](#catalog)

![](/img/virtual9.png)

- [可选] 学习规划硬件计算资源（算你需要买多少服务器）

## 6. Glance

[Catalog](#catalog)

### 6.1 理解 OpenStack 中使⽤的镜像

[Catalog](#catalog)

1. glance 是为 nova 提供镜像服务，以便成功的启动实例，这些镜像是预建的，一般都会预装 cloud-init 的组件，你可以访问 <https://docs.openstack.org/image-guide/obtain-images.html> 来获得更多镜像，默认 glance 会把镜像都放在本地文件系统/var/lib/glance/images/，默认 glance 会把镜像存放在本地文件夹中，当然这样就没有高可用性了，所以 glance 支持对存储后端的配置，我们可以将存储的后台改为 ceph、swift 甚至 aws 的 s3

### 6.2 Glance 基本概念

[Catalog](#catalog)

1. 镜像的后端存储一般对接的是一个对象存储系统
1. 镜像格式
    - raw: 无格式的镜像
    - vhd: 常用的格式，经常被 VMWare，Xen，Microsoft，VirtualBox 来使用的格式
    - vmdk: 另一种被很多虚拟机监控器常用到的格式
    - vdi: 被 VirtualBox 和 Qemu 支持的格式
    - iso: 一个归档的格式的光盘镜像格式
    - qcow2: 被 Qemu 使用的格式，支持复制中写入
    - aki: 表示镜像是亚马逊的 Amazon kernel image
    - ami: 表示镜像是亚马逊的 Amazon machine image
    - ari: 表示镜像是亚马逊的 Amazon ramdisk image
1. glance 核心组件
    - glance-api: 和其他核心项目组件一样都一个管理接口
    - glance-registry: 在 v2 版本，提供存储镜像 metadata 与查找的服务，在 v3 版本被 glance-api 取代

    ![](/img/glance1.png)

### 6.3 Glance 小结

[Catalog](#catalog)

![](/img/glance2.png)

### 6.4 Glance 基本功能

[Catalog](#catalog)

1. 从 OpenStack 下载镜像

    ```bash
    openstack image save --file cirros-disk_x86_64.img cirros-0.5.1-x86_64-disk
    ```

1. 从本地上传镜像

    ```bash
    openstack image create --file cirros-disk_x86_64.img  --container-format bare --disk-format qcow2 myimage
    ```

1. 更新镜像

    ```bash
    openstack image set --min-ram 8 myimage
    ```

1. 删除镜像

    ```bash
    openstack image delete myimage
    ```

1. 创建虚拟机快照（虚拟机快照也是一种镜像）

    ```bash
    openstack server image create --name [instance_snapshot] [instance1]
    ```

    boot from image 的虚拟机，没有云硬盘，系统盘直接落在宿主机上。创建虚拟机快照时，会将系统盘整个变成镜像放到 glance 中，镜像 size 大于 0

    ![](/img/horizon-boot-from-image.png)

    boot from volume 的虚拟机，有云硬盘，系统盘是一个云硬盘（卷 volume）。创建虚拟机快照时，会先创建云硬盘的快照，然后把云硬盘快照 ID 等元数据存入 glance 中，该虚拟机快照里不保存硬盘数据，只保存对应云硬盘快照 ID 等元数据，因此镜像 size 为 0

    ![](/img/horizon-boot-from-volume.png)

## 7. Cinder

[Catalog](#catalog)

### 7.1 理解 Cinder 的作⽤

[Catalog](#catalog)

1. Cinder 为 OpenStack 提供磁盘的服务，当然在 openstack 最小化安装中，您可以选择不安装 cinder，所有的虚拟机的磁盘的数据都会写入到这个虚拟机所启动在的计算节点上的本地磁盘中，就像你使用 kvm 启动一个虚拟机一样有一个虚拟机磁盘文件。但是这样会面临数据丢失的风险，如果这个计算节点上的硬盘坏掉了，那么这个虚拟机的数据就完全丢失了，显然在生产环境中这种情况是非常致命的，所以我们需要 san 的机制将虚拟机的磁盘和计算节点分离开，这样既安全又方便迁移，存储设备很多所以 cinder 需要支持各种存储设备的文件系统. 类似 AWS 的 EBS

### 7.2 Cinder 基本概念

[Catalog](#catalog)

1. cinder 为虚拟机提供管理块存储服务
1. cinder 所支持的存储的文件系统
    - lvm/iscsi
    - ThinLVM
    - NFS
    - NET APP NFS
    - Gluster
    - Dell Equall Logic
    - RBD
1. cinder 核心组件
    - cinder api: 一个基于 http 的管理服务接口，用于接收命令行或者其他组件的的调用
    - cinder scheduler: 服务负责对提供块存储服务器分配任务，当然如果集成了存储的后台有自己的调度的话他的作用就不太重要了
    - cinder volume: 服务负责和存储设备打交道，当它收到 scheduler 发来的消息后，它要处理新建、修改、删除等操作
    - cinder backup: 负责通过驱动和备份的后台打交道，是我们在使用备份的命令的时候，能在正确的位置备份数据

    ![](/img/cinder1.png)

### 7.3 统⼀的存储解决⽅案 Ceph 的简介

[Catalog](#catalog)

1. Ceph 作为 SDS 的解决方案已经是大家公认的做法了，当成本有限的时候 SDS 可以带来很好性能和成本之间的平衡，一般我们的做法是将 glance、cinder 都集成到 ceph 当中

    ![](/img/ceph1.png)

    ![](/img/ceph2.png)

### 7.4 管理卷

[Catalog](#catalog)

1. cinder-volume 可以类比 nova-compute，运行在存储节点（ 定期主动上报容量 ）。cinder-api 运行在控制节点。cinder-schedule（ 默认用空闲容量计算权重 ）类比 nova-schedule（ 默认用空闲内存计算权重 ）。
1. cinder-provider（ 类比 hypervisor ）是独立的，cinder-volume 通过 driver（ 使用哪个 provider 通过 cinder.conf 确定 ） 和 provider 通信。如果有两个 provider，就需要两个不同的 cinder-volume。
1. Create Volume from Source：image / backup / snapshot ？ 增量还是全量？
1. Attach 方案就是 iSCSI，cinder-volume 初始化，nova-compute 来连接。
1. volume -> Image，可以
1. backup：容灾（ restore 是创建空白 volume & copy 数据过去 ），snapshot：便捷回溯
1. nova 的 snapshot 是对系统盘全量备份，生成 image 保存到 glance。Cinder 的 snapshot 依赖与 volume，有 snapshot 的 volume 不可以删除。通常 snapshot 和 volume 放在一起（ volume provider ）
1. NFS provider 里，volume 就是文件

### 7.5 Cinder 基本功能

[Catalog](#catalog)

1. 创建一个空白卷

    ```bash
    openstack volume create --size 2 myvol
    ```

1. 创建一个可以启动的卷（创建卷，并且将 image 中的操作系统复制到新创建的卷中）。该卷可以直接启动 VM，这样一来虚拟机的 root disk 就在云盘上了，就不用担心因为计算节点的硬盘损坏带来的数据丢失的风险

    ```bash
    openstack volume create --size 2 --image [cirros] [myvol]
    ```

1. 为虚拟机添加卷（插入硬盘）

    ```bash
    openstack server add volume [instance1] [vol1]
    ```

    **注意! 虚拟机添加一新的磁盘并不会主动 mount**

    **进入虚拟机操作**


    ```bash
    sudo mkfs.ext3 /dev/vdb   # 格式化硬盘
    sudo mount /dev/vdb /mnt  # 挂载硬盘
    ```

1. 从虚拟机删除卷（拔出硬盘）

    ```bash
    openstack server remove volume [instance1] [vol1]
    ```

1. 创建一个卷的备份

    ```bash
    openstack volume backup create --name [myvol_backup] [myvol]
    ```
1. 从备份中恢复

    ```bash
    openstack volume backup restore [myvol_backup] [myvol1]
    ```
1. 创建：卷的快照

    ```bash
    openstack volume snapshot create --volume [myvol] [myvol_snapshot]
    ```

1. 从快照中创建新卷

    ```bash
    openstack volume create --snapshot [myvol_ss] --size 2 [myvol2]
    ```

### 7.6 Cinder 小结

[Catalog](#catalog)

![](/img/cinder2.png)

### 7.7 备份与快照的差别

[Catalog](#catalog)

1. qcow2 快照 copy-on-write

    ![](/img/cinder3.png)

1. 透过 snapshot 做 rollback 和 rebuild（VM 必须是 boot from image。boot from volume 的 VM 创建的快照 size=0，只能用来重新创建一个 VM，不能原地 rebuild）

    ```bash
    openstack server image create --name my-snapshot --wait my-vm
    openstack image show --fit-width my-snapshot
    openstack server rebuild --image my-snapshot my-vm
    ```

## 8. Neutron

[Catalog](#catalog)

### 8.1 理解 Neutron 的作⽤

[Catalog](#catalog)

1. 一个优秀的 SDN 落地方案

1. neutron 是 OpenStack 项目中负责提供网络服务的组件，它基于软件定义网络的思想，实现了网络虚拟化下的资源管理，在实现上充分利用了 Linux 系统上的各种网络相关的技术，并支持很多第三方的插件

### 8.2 网络概念

[Catalog](#catalog)

1. OSI 架构介绍

    ![](/img/neutron1.png)

    - 封包由上到下依序包装  由下到上依序解包
    - 先解包最外层的封包
1. 网络中的术语
    - tap: 虚拟的网络设备，处理二层数据帧
    - tun: 虚拟的网络设备，处理三层数据包
    - veth: 虚拟的网络线
    - hub: 负责网络总线连接
    - bridge: 也称作交换机 (switch) 根据 mac table 转发数据，如 linuxbridge，OpenVSwitch
    - router: 处理转发三层子网上的报文，原理是根据内部的路由转发表将从一个网络接口中收到的数据包转发到另一个网络接口
    - network namespace: 逻辑上是网络堆栈的一个副本，它有自己的路由、防火墙规则和网络设备，默认情况下，子进程继承其父进程的 network namespace

1. arp broadcast，TCP handshacking，Linux Bridge，OVS Bridge

1. 创建两台虚机能互通的网络

    ![](/img/neutron2.png)

    ```console
    # add the namespaces
    $ ip netns add ns1
    $ ip netns add ns2
    # create the veth pair
    $ ip link add tap1 type veth peer name tap2
    # move the interfaces to the namespaces
    $ ip link set tap1 netns ns1
    $ ip link set tap2 netns ns2
    # bring up the links
    $ ip netns exec ns1 ip link set dev tap1 up
    $ ip netns exec ns2 ip link set dev tap2 up
    # now assign the ip addresses
    $ ip netns exec ns1 ip addr add 192.168.0.2/24 dev tap1
    $ ip netns exec ns2 ip addr add 192.168.0.3/24 dev tap2
    # ping to each other
    $ ip netns exec ns1 ping 192.168.0.3
    ```

1. 透过 linux bridge 创建两台虚机能互通的网络

    ![](/img/neutron3.png)

    ```console
    $ ip netns add ns1
    $ ip netns add ns2
    # create the switch
    $ BRIDGE=br-test
    $ brctl addbr $BRIDGE
    $ brctl stp   $BRIDGE off
    $ ip link set dev $BRIDGE up
    #### PORT 1
    # create a port pair
    $ ip link add tap1 type veth peer name br-tap1
    # attach one side to linuxbridge
    $ brctl addif br-test br-tap1
    # attach the other side to namespace
    $ ip link set tap1 netns ns1
    # set the ports to up
    $ ip netns exec ns1 ip link set dev tap1 up
    $ ip link set dev br-tap1 up
    #### PORT 2
    # create a port pair
    $ ip link add tap2 type veth peer name br-tap2
    # attach one side to linuxbridge
    $ brctl addif br-test br-tap2
    # attach the other side to namespace
    $ ip link set tap2 netns ns2
    # set the ports to up
    $ ip netns exec ns2 ip link set dev tap2 up
    $ ip link set dev br-tap2 up
    # now assign the ip addresses
    $ ip netns exec ns1 ip addr add 192.168.0.2/24 dev tap1
    $ ip netns exec ns2 ip addr add 192.168.0.3/24 dev tap2
    # ping to each other
    $ ip netns exec ns1 ping 192.168.0.3
    ```

1. 透过 OVS Bridge 创建两台虚机能互通的网络

    ![](/img/neutron4.png)

    ```console
    # add the namespaces
    $ ip netns add ns1
    $ ip netns add ns2
    # create the switch
    $ BRIDGE=ovs-test
    $ ovs-vsctl add-br $BRIDGE
    #### PORT 1
    # create a port pair
    $ ip link add tap1 type veth peer name ovs-tap1
    # attach one side to ovs
    $ ovs-vsctl add-port $BRIDGE ovs-tap1
    # attach the other side to namespace
    $ ip link set tap1 netns ns1
    # set the ports to up
    $ ip netns exec ns1 ip link set dev tap1 up
    $ ip link set dev ovs-tap1 up
    #### PORT 2
    # create a port pair
    $ ip link add tap2 type veth peer name ovs-tap2
    # attach one side to ovs
    $ ovs-vsctl add-port $BRIDGE ovs-tap2
    # attach the other side to namespace
    $ ip link set tap2 netns ns2
    # set the ports to up
    $ ip netns exec ns2 ip link set dev tap2 up
    $ ip link set dev ovs-tap2 up
    # now assign the ip addresses
    $ ip netns exec ns1 ip addr add 192.168.0.2/24 dev tap1
    $ ip netns exec ns2 ip addr add 192.168.0.3/24 dev tap2
    # ping to each other
    $ ip netns exec ns1 ping 192.168.0.3
    ```

1. 透过 neutron 创建两台虚机能互通的网络
    - Neutron ML2.OVS_agent，L3_agent，dhcp_agent 疯了...

    ![](/img/neutron5.png)

### 8.3 Neutron 基本概念

[Catalog](#catalog)

1. neutron 核心组件
    - neutron-server: 提供 API 接口，并把对 API 的调用请求传给已经配置好的插件进行后续处理. 插件需要访问数据库来维护各种配置数据和对应关系，例如路由器、网络、子网、端口、floating ip、安全组等等
    - (neutron-)plugin: 维护逻辑网络状态，调用 agent，处理 server 请求
    - neutron-agent: 负责在 network-provider 上实现网络拓璞，处理 plugin 请求
    - network-provider: 网络设备，可以是物理或是虚拟，提供网络服务
    - neutron-dhcp-agent: 通过 dnsmasq 进程（轻量级服务器，可以提供 dns、dhcp、tftp 等服务）来实现的，该进程绑定到 dhcp 命名空间中的 br-int 的接口上，可以查看相关的进程
    - neutron-l3-agent: 负责项目(租户)网络和 floating ip 之间的地址转换的服务，它通过 Linux iptables 的 SNAT、DNAT 来完成地址的双向转换

    ![](/img/neutron6.png)

1. Plugin 和 Agents
    - Q: plugin 和 agents 是否是一对? 是的
    - A: plugin 有分core plugin 和 service plugin，service_plugins = router，core_plugin = ml2

    - Q: 一个plugin 可管理多个agents? 看neutron.conf
    - A:  dhcp_agents_per_network = 1 max_l3_agents_per_router = 3

    - Q: 一个plugin 可以支援多种不同的agents吗? 可以
    - A: ml2

1. ml2 plugin 介绍
    - ML2 提供 neutron 异构部署的可能性，可以在不同的节点部署不同的网络架构
    - Type Driver: 决定逻辑网络类型
    - Techanism Driver: 决定如何在 provider 实现网络类型的办法

    ![](/img/neutron7.png)

    ```console
    $ cat plugins/ml2/ml2_conf.init
    [ml2]
    tenant_network_types = vxlan
    extension_drivers = port_security
    mechanism_drivers = openvswitch,linuxbridge
    type_drivers = local,flat,vlan,gre,vxlan,geneve

    [ml2_type_flat]
    flat_networks = public,

    [ml2_type_vlan]
    network_vlan_ranges = public

    [agent]
    tunnel_types = vxlan
    root_helper_daemon = sudo /usr/local/bin/neutron-rootwrap-daemon /etc/neutron/rootwrap.conf
    root_helper = sudo /usr/local/bin/neutron-rootwrap /etc/neutron/rootwrap.conf

    [ovs]
    datapath_type = system
    bridge_mappings = public:br-ex
    tunnel_bridge = br-tun
    local_ip = 172.16.60.17
    ```

### 8.4 ⽣产环境中的实施⽅案

[Catalog](#catalog)

1. Linux Bridge 支持 vlan & vxlan

### 8.5 理解节点的内部⽹络的实现

[Catalog](#catalog)

1. neutron 术语
    - br-int: 综合网桥当我们使用 ovs 的时候，ovs 会根据配置文件创建一个综合网桥，目的是把虚拟机的流量引向这座综合网桥
    - qbr: 也是网桥，不过针对 Security group 通常在 linux bridge 上实现 iptables
    - br-tun: ovs 的虚拟网桥，接收 br-int 透过穿遂技术与对象 br-tun 形成通道，实现虚拟三层网络
    - br-ex: 使用ovs的时候，负责openstack南北向的流量，会和一张物理网卡绑定
    - GRE: General Routing Encapsulation，一种通过封装来实现隧道的方式
    - qvb: neutron的veth，使用 Linux Bridge 作为插件的时候使用的虚拟接口
    - qvo: neutron的veth，使用 ovs 作为插件的时候使用的虚拟接口。
    - iptables: Linux 上常见的实现安全策略的防火墙软件，实例通过 br-ex 前都会通过 iptables 实现 Nat 地址转换
    - namespace: 用来实现隔离的一套机制，不同 namespace 中的资源之间彼此不可见

    ![](/img/neutron10.png)

    ![](/img/neutron11.png)

    ![](/img/neutron12.png)

### 8.6 [可选] Distributed Virtual Router

[Catalog](#catalog)

1. Before
    - Neutron Routing: Neutron Server 透过 Linux IP Stack 和 iptables 執行 L3 轉發和 NAT Neutron Server 与 Network Node交互实现 高可用性
    - 问题: 网路管理的过程当中 某Neutron Node宕机会如何? 会成为NAT的阻塞点!!

    ![](/img/neutron8.png)

1. After
    - 把原本 Network node 的工作分散到了 Compute Node 上
    - 南北流量 Floating IP 可选择在计算节点上处理
    - 东西流量不用可选择不用经过网路节点上
    - 大幅降低网络节点工作量,提升性能,带宽与高容错率

    ![](/img/neutron9.png)

    ```console
    cat /etc/neutron.conf
        # System-wide flag to determine the type of router that tenants can create.
        # Only admin can override. (boolean value)
        router_distributed = true

    cat l3_Agent.ini

        # Possible values:
        # dvr - <No description provided>
        # dvr_snat - <No description provided>
        # legacy - <No description provided>
        # dvr_no_external - <No description provided>
        agent_mode = dvr_snat

        cat L2_agent.ini
        enable_distributed_routing = True
    ```

### 8.7 [可选] ⽹络加速的技术 dpdk、sr-iov、TSN 的介绍

[Catalog](#catalog)

1. DPDK 是什么?
1. 为什么要整 DPDK? OVS had kernel overhead and kernel bottleneck

    ![](/img/neutron13.png)

1. 实现 DPDK 需满足以下
    - 需要特别网卡，包含的驱动如: e1000，ixgbe i40e
    - 需要特别分配cpu，大页内存(Huge memory)，和 DPDK NIC 给 DPDK 使用

    ![](/img/neutron14.png)

1. sr-iov 是什么?
1. 为什么要搞 sr-iov? Network controller is transparent to physical device

    ![](/img/neutron15.png)

1. 实现 DPDK 需满足以下
    - 需要特别网卡，包含的驱动如: e1000，ixgbe i40e
    - 底层创建 PF 跟 VF
1. TSN 是什么?
1. 怎么又来了一个，他能做什么? Time synchronization
1. TSN标准 (IEEE 802.1 IEEE 1588)
    - 提高同步性能
    - 数据帧抢占优先
    - 提升规划的通信!!
    - 无缝冗余(HSR)
    - 高速通道带宽预留
1. 示例
    - 边缘云跟边缘传感设备
    - p2p4l，phc2sys: LinuxPTP项目提供的时间同步工具
    - tc(traffic control): IPROUTE2提供，控制数据帧的
    - TSN Sender/Receiver: 发送与接收TSN数据

    ![](/img/neutron16.png)

### 8.8 Neutron 基本功能

[Catalog](#catalog)

1. 创建外部网络

    ```bash
    openstack network create --enable --provider-network-type [flat]  --provider-physical-network [br-ex name] --project admin --external  [network-name]
    ```

    ![](/img/horizon-external-network.png)

1. 创建外部网络的子网

    ```bash
    openstack subnet create --subnet-range [192.168.100.0/24] --gateway [192.168.100.1] --dhcp --network [public] [pubsub]
    ```

    ![](/img/horizon-external-subnet.png)

    ![](/img/horizon-external-ip-range.png)

1. 租户网络实验

    ```bash
    # 1. 创建私有网络（子网)
    openstack network create testNetwork2
    openstack subnet create --network testNetwork2 --subnet-range 192.168.20.0/24 testSubnet2

    # 2. 基于子网创建 VM（这个之前做过，可以用界面完成）

    # 3. 创建路由
    openstack router create testRouter2

    # 4. 为路由器设置网关（连接到外网）
    openstack router set --external-gateway public --enable-snat testRouter2

    # 5. 路由增加接口绑定到私有网络（租户网络）的子网
    openstack router add subnet testRouter2 testSubnet2
    ```

    第 5 步对应到界面是（注意，**第 4 步为路由器设置网关不要和第 5 步连接租户网络混淆，连接外网必须用设置网关，不能在路由器上添加对外网的接口**）：

    ![](/img/horizon-router-add-interface.png)

1. 浮动 IP 实验

    ```bash
    # 1. 创建 FIP
    openstack floating ip create public

    # 2. 绑定 FIP
    openstack server add floating ip [testInstance2] [172.25.0.99]

    # 3. [可选]此时可以进 router 的 network namespace 看到 DNAT，以及 FIP 实际配置在 router 上
    ip netns list
    ip netns exec [qrouter-9dd0fd27-17c7-4e41-a4dc-9612d23266c9] iptables -t nat -L -v -n
    ip netns exec [qrouter-9dd0fd27-17c7-4e41-a4dc-9612d23266c9] ip a

    # 4. 解绑 FIP
    openstack server remove floating ip testInstance222 172.25.0.99
    ```

实验作业：

1. 删除外部网络（先 router 上 clear gateway，再删除 public 网络），然后创建 public 网络，新建 cirros VM，确认 cirros VM 可以 ping 通宿主机（172.25.0.10）
2. 新建一个租户网络，router 上增加连接此租户网络的 interface，新建 cirros VM，确认 cirros VM 可以 ping 通宿主机（172.25.0.10）
3. 对 cirros VM 绑定浮动 IP，修改安全组，确认从宿主机（172.25.0.10）可以 ping 通 cirros VM 的浮动 IP

### 8.9 管理安全组规则

[Catalog](#catalog)

## 9. devstack 服务的管理

[Catalog](#catalog)

1. https://docs.openstack.org/tacker/latest/install/devstack.html
1. https://docs.openstack.org/devstack/latest/

### 9.1 理解 devstack 的作⽤

[Catalog](#catalog)

1. DevStack 是一系列可扩展的脚本，用于基于 git master 的最新版本快速调出完整的 OpenStack 环境。它以交互方式用作开发环境和 OpenStack 项目大部分功能测试的基础。

### 9.2 Devstack 基本概念

[Catalog](#catalog)

1. devstack 透过执行 stack.sh 脚本，搭建 openstack 环境，依据 local.conf 参数，决定提供哪些服务
1. 使用 systemd 来管理 devstack 部署的 OpenStack
1. DevStack 插件。支持额外的 Openstack 服务，以插件接口的概念，扩展 openstack 服务

### 9.3 Devstack 基本功能

[Catalog](#catalog)

1. 重启 glance api 服务

    ```console
    # 检查服务
    $ systemctl list-unit-files | grep "devstack@*"

    # 重启 glance api 服务
    $ systemctl restart "devstack@g-api"

    # 查看 glance api 状态
    $ systemctl status "devstack@g-api"
      devstack@g-api.service - Devstack devstack@g-api.service
       Loaded: loaded (/etc/systemd/system/devstack@g-api.service; enabled; vendor preset:
       Active: active (running) since Sat 2021-05-29 08:25:20 UTC; 2h 56min ago
       Main PID: 18213 (glance-api)
       Tasks: 3 (limit: 4915)
       CGroup: /system.slice/system-devstack.slice/devstack@g-api.service
           ├─18213 /usr/bin/python3.6 /usr/local/bin/glance-api --config-dir=/etc/glan
           ├─18450 /usr/bin/python3.6 /usr/local/bin/glance-api --config-dir=/etc/glan
           └─18451 /usr/bin/python3.6 /usr/local/bin/glance-api --config-dir=/etc/glan
    ```

1. 添加 plugin，提供 swift 服务

    ```console
    vi local.conf

        ...
        [[local|localrc]]
        ...
        # Swift
        # -----
        SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5
        SWIFT_REPLICAS=1
        SWIFT_DATA_DIR=$DEST/data
        enable_service s-proxy s-object s-container s-account

    # 部署
    $ ./stack.sh
    ```

### 9.4 Debug

[Catalog](#catalog)

1. 场景：创建一个 port，固定 IP & MAC，MAC 11:22:33:44:55:66，创建 VM，指定这个 Port，会报错。

    ```bash
    journalctl -f -u devstack@n-cond.service
    journalctl -f -u devstack@n*
    journalctl -f -u devstack@n* > ~/a.txt
    ```

    ```
    Jul 28 16:48:10 test-coa-5 nova-conductor[7519]: 2020-07-28 16:48:10.626 8393 ERROR nova.scheduler.utils [req-9b59c38d-c943-4d56-82ca-5cf9f1b5bfe9 cee4ec5181d24cc2a3a3c4975c3277a2 4452a8c2601b482fb13639c8839c80f9 - default default] [instance: a5a972b4-b779-4931-94c3-c43956f4d7ee] Error from last host: test-coa-5 (node test-coa-5): [u'Traceback (most recent call last):\n', u'  File "/opt/stack/nova/nova/compute/manager.py", line 1996, in _do_build_and_run_instance\n    filter_properties)\n', u'  File "/opt/stack/nova/nova/compute/manager.py", line 2237, in _build_and_run_instance\n    instance_uuid=instance.uuid, reason=six.text_type(e))\n', u"RescheduledException: Build of instance a5a972b4-b779-4931-94c3-c43956f4d7ee was re-scheduled: XML error: expected unicast mac address, found multicast '11:22:33:44:55:66'\n"]
    ```

## 10. Swift

[Catalog](#catalog)

### 10.1 理解 Swift 的使⽤场景

[Catalog](#catalog)

1. Swift 为 Openstack 提供对象存储，透过调用 API 实现存储和检索大量数据。 Swift 将数据存储为二进制对象。像 AWS S3。


### 10.2 Swift 基本概念

[Catalog](#catalog)

1. swift 核心组件
    - Proxy service: 一个管理接口，处理 REST API 请求
    - Accounts service: 一组 account database 管理 container 列表
    - Containers service: 一组 container database 管理 object 列表
    - Objects service: 数据本身

    ![](/img/swift1.png)

1. 每个存储节点上的设备被 swift 暴露出来称为一个存储设备，swift 通过 ring 的算法将每个设备 hash 得到一个值，很多设备从最小的 hash 到最大组成了一个环，然后将要上传对象的 Account、Container 和 Object 一起 hash 出来一个值，放入环中，按照向左的原则找到一个存储 Driver 对应的设备的 ip 地址和位置，将文件存入

1. Rings: Map logical names of data to locations on particular disks.

    ![](/img/swift2.png)

    ![](/img/swift3.png)

### 10.3 Swift 基本功能

[Catalog](#catalog)

1. 查询 swift 状态

    ```console
    $ swift -V 3 stat
                   Account: AUTH_0ae8ec62a38b4ccf99f40d5308064023
                Containers: 0
                   Objects: 0
                     Bytes: 0
              Content-Type: text/plain; charset=utf-8
               X-Timestamp: 1622289439.60654
           X-Put-Timestamp: 1622289439.60654
                      Vary: Accept
                X-Trans-Id: tx0d86462bd35a488d88809-0060b22c1f
    X-Openstack-Request-Id: tx0d86462bd35a488d88809-0060b22c1f
    ```

1. swift 创建 container

    ```console
    $ openstack container create my_container
    ```

1. 上传下载一对象

    ```console
    $ openstack object create --name test.txt my_container coa.txt
    $ openstack object save --file test.txt my_container test.txt
    ```

    ```console
    $ swift -V 3  upload demo-container1 hello_swift.txt
    $ swift -V 3 list
    $ swift -V 3 download demo-container1 Imback_swift.txt
    ```

### 10.4 [可选] 管理到期的对象

[Catalog](#catalog)


## 11. Heat

[Catalog](#catalog)

### 11.1 Heat 的模版中的讲解

[Catalog](#catalog)

1. heat 是 OpenStack 核心组件中的一个，它可以实现自动的在我们的 OpenStack 环境中创建资源，比如虚拟机、网络、虚拟路由、安全等资源，也是很多 OpenStack 周边的项目需要依赖的项目，比如 Tacker 等等

### 11.2 Heat 基本概念

[Catalog](#catalog)

1. heat 核心组件

    - heat-api: heat-api 组件提供了一个 OpenStack 原生 REST API，它通过通过 RPC 将 API 请求发送到热引擎来处理 API 请求
    - heat-api-cfn: heat-api-cfn 组件提供了一个与 AWS CloudFormation 兼容的 AWS 查询 API，并通过通过 RPC 将 API 请求发送到热引擎来处理 API 请求
    - heat-engine: heat-engine 的主要职责是协调模板的启动并将事件提供给 API 使用者

    ![](/img/heat1.png)

1. heat 模版默认以 yaml 格式编辑

    - heat_template_version: 重要! 不仅告诉 Heat 模板的格式，还告诉 Heat 将被验证和支持的功能
    - description: 可选，功能描述
    - parameters: 宣告变量，可在 resources 模块使用
    - resources: 宣告需要使用的资源

1. https://docs.openstack.org/heat/latest/template_guide/hot_spec.html

1. https://docs.openstack.org/heat/latest/template_guide/basic_resources.html


### 11.3 Heat 基本功能

[Catalog](#catalog)

1. 使用 heat 模版创建 OpenStack 的资源

    ```console
    $ vi cirros_heat_template.yaml

    heat_template_version: 2018-08-31

    description: create a cirros vm through heat template

    parameters:
      instance_type:
        type: string
        description: Instance type for WordPress server
        default: m1.tiny
      image_id:
        type: string
        description: cirros cloud image
        default: cirros-0.5.1-x86_64-disk

    resources:
      instance_port:
        type: OS::Neutron::Port
        properties:
          network: public
          security_groups:
            - default
          fixed_ips:
            - subnet_id: public-subnet
      cirros_instance:
        type: OS::Nova::Server
        properties:
          image: { get_param: image_id }
          flavor: { get_param: instance_type }
          networks:
            - port: { get_resource: instance_port }

    outputs:
      instance_name:
        value: { get_attr: [cirros_instance, name] }
      instance_ip:
        value: { get_attr: [cirros_instance, first_address] }

    # 透过 heat template 创建虚拟机

    $ openstack stack create -t cirros_heat_template.yaml teststack
      id: a5a78571-5f47-4d09-ac9a-5a547c8d0927
      stack_name: teststack
      description: create a cirros vm through heat template
      creation_time: '2021-08-05T12:25:17Z'
      updated_time: null
      stack_status: CREATE_IN_PROGRESS
      stack_status_reason: Stack CREATE started

    $ openstack stack show teststack
      ...
      | stack_status_reason   | Resource CREATE failed: StackValidationFailed: resources.instance_port: Property error: instance_port.Properties.fixed_ips[0]: Unable to find subnet with name or id 'subnet_heat' |
      ...

    $ openstack stack update teststack --existing
      +---------------------+------------------------------------------+
      | Field               | Value                                    |
      +---------------------+------------------------------------------+
      | id                  | a5a78571-5f47-4d09-ac9a-5a547c8d0927     |
      | stack_name          | teststack                                |
      | description         | create a cirros vm through heat template |
      | creation_time       | 2021-08-05T12:25:17Z                     |
      | updated_time        | 2021-08-05T12:31:49Z                     |
      | stack_status        | UPDATE_IN_PROGRESS                       |
      | stack_status_reason | Stack UPDATE started                     |
      +---------------------+------------------------------------------+

    $ openstack stack list
      +--------------------------------------+------------+----------------------------------+-----------------+----------------------+----------------------+
      | ID                                   | Stack Name | Project                          | Stack Status| Creation Time        | Updated Time         |
      +--------------------------------------+------------+----------------------------------+-----------------+----------------------+----------------------+
      | a5a78571-5f47-4d09-ac9a-5a547c8d0927 | teststack  | d69bb3c9954f49f991565dde26d8e8cb | UPDATE_COMPLETE| 2021-08-05T12:25:17Z | 2021-08-05T12:31:49Z |
      +--------------------------------------+------------+----------------------------------+-----------------+----------------------+----------------------+
      $ openstack server list
      +--------------------------------------+----------------------------------------+--------+-----------------------+--------------------------+---------+
      | ID                                   | Name                                   | Status | Networks        | Image                    | Flavor  |
      +--------------------------------------+----------------------------------------+--------+-----------------------+--------------------------+---------+
      | 587a8c5c-2041-4d09-bde0-a04c5ed67e7f | teststack-cirros_instance-ojqijaffb2pm | ACTIVE | public=192.168.191.44 | cirros-0.5.1-x86_64-disk | m1.tiny |
      +--------------------------------------+----------------------------------------+--------+-----------------------+--------------------------+---------+

    $ openstack stack output show --all teststack
    +---------------+------------------------------------------------------------+
    | Field         | Value                                                      |
    +---------------+------------------------------------------------------------+
    | instance_name | {                                                          |
    |               |   "output_key": "instance_name",                           |
    |               |   "description": "No description given",                   |
    |               |   "output_value": "teststack-cirros_instance-ouyeeodkjq2r" |
    |               | }                                                          |
    | instance_ip   | {                                                          |
    |               |   "output_key": "instance_ip",                             |
    |               |   "description": "No description given",                   |
    |               |   "output_value": "172.25.0.231"                           |
    |               | }                                                          |
    +---------------+------------------------------------------------------------+

    $ openstack stack delete teststack
      Are you sure you want to delete this stack(s) [y/N]? y

    $ openstack server list
      (empty)
    ```

    ![](/img/heat2.png)

    ![](/img/heat3.png)

### 11.4 其它

[Catalog](#catalog)

- 更新⼀个模版
- 创建互相依赖 yaml 模版

## 12. Quiz

[Catalog](#catalog)

### 模拟题讲解

[Catalog](#catalog)

### 模拟题练习

[Catalog](#catalog)

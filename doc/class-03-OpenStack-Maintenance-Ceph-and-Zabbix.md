# 部署和运维

## Neturon 与 SDN

- Neutron 的概念空间中有哪些对象？
- Neutron 由模块组成？
- Neutron 由几种网络模型？
- VLAN & 物理 L3 的网络模型是怎样的？
- 基于 Linux Bridge 的网络模型是怎样的？
- 基于 OVS 的网络模型是怎样的？
- 如何查看流表？流表的基本操作（ 增删查改 ）？
- 安全组在底层的实现是怎样的？
- FWaaS 在底层的实现是怎样的？
- VXLAN 模型是什么？在 OpenStack 底层是怎么实现的？适用于哪些场合？
- GRE 模型是什么？在 OpenStack 底层是怎么实现的？适用于哪些场合？
- DPDK 怎么支持？
- SRIOV 怎么支持？
- IPv6 的支持情况如何？后端怎么启用 IPv6 支持？前端用户怎么使用（ API & 命令行 ）？

## Manila

- [Manila 提供什么服务？](https://docs.openstack.org/manila/latest/#what-is-manila) Providing Shared Filesystems as a service，[NAS 存储](https://baike.baidu.com/item/NAS/3465615)。对照的 AWS 服务是什么？[Amazon Elastic File System (EFS)](https://aws.amazon.com/cn/efs/)
- Manila 支持哪些文件共享协议？主要是 [NFS，CIFS](https://www.dell.com/community/%E5%85%A5%E9%97%A8%E7%BA%A7%E5%92%8C%E4%B8%AD%E7%AB%AF/%E5%88%86%E4%BA%AB-CIFS%E5%92%8CNFS%E7%9A%84%E5%8C%BA%E5%88%AB/td-p/6934849)，通过不同的后端驱动实现。还有[其它协议](https://docs.openstack.org/manila/latest/admin/shared-file-systems-share-management.html)。
- [Manila 的概念空间里有什么对象？](https://docs.openstack.org/manila/latest/admin/shared-file-systems-key-concepts.html)
    - **Share**：The fundamental resource unit allocated by the Shared File System service. It represents an allocation of a persistent, readable, and writable filesystems. Compute instances access these filesystems
    - **Share Instance**：This concept is tied with share and represents created resource on specific back end, when share represents abstraction between end user and back-end storages.
    - **Snapshot**
    - **Storage Pools**：The storage may present one or more logical storage resource pools that the Shared File Systems service will select as a storage location when provisioning shares
    - **Share Type**：An abstract collection of criteria used to characterize share
    - **Share Access Rules**：Define which users can access a particular share
    - **Security Services**：Allow granular client access rules for administrators，[参考](https://docs.openstack.org/manila/latest/admin/shared-file-systems-security-services.html)
    - **Share Server**：A logical entity that hosts the shares created on a specific share network
- [Manila 由几个模块组成？](https://docs.openstack.org/security-guide/shared-file-systems/intro.html)

    ![](../img/manila-intro.png)

    - **manila-api**
    - **manila-data**：类似 nova-conductor，This service is responsible for managing data operations which may take a long time to complete and block other services if not handled separately.
    - **manila-scheduler**：Responsible for scheduling and routing requests to the appropriate manila-share service. It does that by picking one back-end while filtering all except one back-end.
    - **manila-share**：类似 nova-compute，Responsible for managing Shared File Service devices, specifically the back-end devices.
- Manila 如何创建文件共享，以及如何让该共享被 VM Instance 访问？
- [实验] Manila 共享存储的配置和使用具体操作

## OpenStack 高可用部署

- 商用中较为流行的 OpenStack HA 方案有哪些？
- 基础设施的 HA 方案推荐怎么做？
- 控制节点的 HA 方案推荐怎么做？
- 网络节点的 HA 方案推荐怎么做？

## 虚机注入的方式

## 虚机镜像存储方式，需要解决分布式读写延迟对业务的影响

## 客户的最佳实践和遇到的问题



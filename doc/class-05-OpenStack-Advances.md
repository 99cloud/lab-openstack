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

### 2.3 Kolla Ansible

[返回目录](#课程目录)

## 3. 运维

[返回目录](#课程目录)

### 3.1 OpenStack Ansible

[返回目录](#课程目录)

### 3.2 小版本升级

[返回目录](#课程目录)

### 3.3 扩缩容

[返回目录](#课程目录)

### 3.4 基础组件运维

[返回目录](#课程目录)

#### 3.4.1 MarialDB

[返回目录](#课程目录)

#### 3.4.2 RabbitMQ

[返回目录](#课程目录)

#### 3.4.3 Prometheus

[返回目录](#课程目录)

#### 3.4.4 EFK

[返回目录](#课程目录)

## 4. 排错

[返回目录](#课程目录)

### 4.1 日志查询

[返回目录](#课程目录)

### 4.2 服务异常检测

[返回目录](#课程目录)

### 4.3 存储异常

[返回目录](#课程目录)

### 4.4 网络异常

[返回目录](#课程目录)

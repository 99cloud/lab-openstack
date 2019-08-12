# kolla 运维相关

## 使用 kolla 升级 openstack 版本

### 简介

- 使用 kolla 部署的 openstack 升级相对简单，但不是所有组件都支持的。有的组件可能会升级失败，这个完全取决于每个组件的自己实现方式。升级分为两个步骤:
	1. 修改 globals.yml 文件，更换其中的 release 版本为最新的版本
	2. 应用 upgrade
- kolla 升级本质上是强制刷新数据库，然后在替换掉对应的容器。

### 步骤
- 修改 `/etc/kolla/globals.yml` 文件，把 stein 版本升级到master分支

		openstack_release: "master"
- 执行upgrade

		[root@openstack ~]# kolla-ansible -i ~/multinode upgrade

## kolla 扩容步骤

1. 首先安装操作系统
2. 安装完操作系统之后，配置 hosts 文件，以及网卡
3. 如果是 cinder 的 lvm 后端，则需要准备 vg
4. 如果该节点也作为 ceph 节点，则需要给磁盘打标签
5. 接下来在 deploy 节点上操作（ 一般是 control01 ）
	- 设置 ssh 免密

			[root@control01 ~]# ssh-copy-id root@<your new node>
	- 修改 multinode 文件

			#把节点加入到multinode文件中
			#比如该节点是计算存储节点，则把该主机加入到compute组和storage组中
			vim ~/multinode
	- 安装docker等所需要包

			kolla-ansible  -i ~/multinode bootstrap-servers
	- 部署

			kolla-ansible -i ~/multinode deploy
	- 检查节点是否成功

			[root@openstack ~]# nova service-list
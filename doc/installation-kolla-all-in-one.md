# 硬件环境准备

1. CPU / 内存 / 磁盘
	- 最小配置为：4C / 8G / 50G
	- 建议使用 16G 以上内存，如果开启cinder的LVM后端，需要在加一块磁盘。
2. 网络配置最少需要2个网口
	- 一个是管理网
	- 一个虚拟机业务网
3. 操作系统 CentOS 7 以上系统，本文档是使用 CentOS 来做 demo。
4. 操作系统需要能够访问外部网络
5. 关闭 selinux 和 firewalld

# 安装前准备

1. 修改 hosts 文件，把 hostname 对应的 ip 地址，添加到这个文件中。

	```
	[root@openstack-allinone ~]# cat /etc/hosts
	127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
	::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
	10.211.55.9 openstack-allinone
	[root@openstack-allinone ~]#
	```
2. 安装 epel-release

	```
	sudo yum install -y epel-release
	```
3. 安装 python 依赖

	```
	sudo yum install -y python-devel libffi-devel gcc openssl-devel libselinux-python
	```
4. 安装虚拟环境（可选）
	- 目前 kolla 以及 ansible 支持安装在虚拟环境中

		```
		sudo yum install -y python-virtualenv
		```
	- 如果直接安装在裸机中，可以不安装虚拟环境。本例没有使用虚拟环境
5. 安装 ansible（2.5+版本）
	- 目前 kolla 已经不再支持 2.5 以下的 ansible 的版本

		```
		easy_install pip    //安装pip
		pip install -U pip  //确保使用最新的pip
		pip install ansible  //安装ansible
		```
	- 国内 pip 安装速度较慢的话，可以使用国内的 pip 源

		```
		pip install ansible  -i https://pypi.tuna.tsinghua.edu.cn/simple
		```
	- 检查 ansible 版本

		```
		[root@openstack-allinone ~]# ansible --version
		ansible 2.8.2
		  config file = None
		  configured module search path = [u'/root/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
		  ansible python module location = /usr/lib/python2.7/site-packages/ansible
		  executable location = /usr/bin/ansible
		  python version = 2.7.5 (default, Jun 20 2019, 20:27:34) [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
		[root@openstack-allinone ~]#
		```

# 安装 kolla-ansible

1. 本次安装最新的发布版本 stein 版本，所以我们使用 stein 版本的 kolla-ansible
2. 如果操作系统没有安装 git 需要首先安装 git

	```
	yum install -y git
	```
3. 之后克隆 kolla-ansible 的代码

	```
	git clone https://github.com/openstack/kolla-ansible.git -b stable/stein
	```
4. 该步骤如果克隆较慢，可以自己下载压缩包，或者配置 git 代理

	```
	[root@openstack-allinone kolla-ansible]# git branch //检查分支
	* stable/stein
	[root@openstack-allinone kolla-ansible]# pwd
	/root/kolla-ansible
	[root@openstack-allinone kolla-ansible]#
	```
4. 安装 kolla-ansible

	```
	cd ~/kolla-ansible
	pip install . -i https://pypi.tuna.tsinghua.edu.cn/simple
	```
5. 创建配置文件目录

	```
	sudo mkdir -p /etc/kolla
	sudo chown $USER:$USER /etc/kolla
	```
6. 拷贝 globals.yml 和 passwords.yml 文件到 /etc/kolla 目录下

	```
	cp -r /usr/share/kolla-ansible/etc_examples/kolla/* /etc/kolla
	```
7. 拷贝 allinone 和 mutinode 文件到当前家目录下

	```
	cp /usr/share/kolla-ansible/ansible/inventory/* ~/
	```

# 配置 Inventory 和 globals.yml 文件

1. 在allinone的安装过程中不需要修改Inventory文件
2. 修改globals.yml文件

	```
	vi /etc/kolla/globals.yml
	修改如下选项
	kolla_install_type: "source"
	openstack_release: "stein"
	kolla_internal_vip_address: "10.211.55.100" //这个ip需要是管理网同一个网段的
	network_interface: "eth0"
	neutron_external_interface: "eth1"
	enable_cinder: "yes"
	enable_cinder_backend_lvm: "yes"
	   ......其他的默认即可
	```

#  配置 cinder 的 backend

1. cinder 默认使用的是 cinder-volumes 这个 vg，这个 vg 需要手动创建

	```
	[root@openstack-allinone ~]# lsblk
	NAME                 MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
	sda                    8:0    0   128G  0 disk
	├─sda1                 8:1    0   500M  0 part /boot
	└─sda2                 8:2    0 127.5G  0 part
	  ├─VolGroup-lv_root 253:0    0    50G  0 lvm  /
	  ├─VolGroup-lv_swap 253:1    0     2G  0 lvm  [SWAP]
	  └─VolGroup-lv_home 253:2    0  75.5G  0 lvm  /home
	sdb                    8:16   0   100G  0 disk
	sr0                   11:0    1 146.4M  0 rom
	sr1                   11:1    1   603M  0 rom
	```
2. 使用 sdb 创建 pv

	```
	[root@openstack-allinone ~]# pvcreate /dev/sdb
	  Physical volume "/dev/sdb" successfully created
	[root@openstack-allinone ~]#
	```
3. 创建 vg

	```
	[root@openstack-allinone ~]# vgcreate cinder-volumes /dev/sdb
	  Volume group "cinder-volumes" successfully created
	[root@openstack-allinone ~]#
	```

# 部署 openstack

1. 执行 bootstrap，会安装 docker 一类所需要的工具

	```
	kolla-ansible  bootstrap-servers //默认使用allinone文件
	```
2. 确认cpu是否支持硬件虚拟化

	```
	grep -E 'svm|vmx' /proc/cpuinfo
	#如果有回显，则下面的操作不需要，如果没有回显，说明cpu不支持硬件虚拟化，需要修改virt_type
	mkdir -p /etc/kolla/config/nova
	cat << EOF > /etc/kolla/config/nova/nova-compute.conf
	[libvirt]
	virt_type=qemu
	cpu_mode = none
	EOF
	```
3. docker 是从 docker hub 上面 pull openstack 镜像，国内的环境有点慢，所以这里配置了 docker 加速，当然也可以不配置这个步骤

	```
	sudo mkdir -p /etc/docker
	sudo tee /etc/docker/daemon.json <<-'EOF'
	{
	  "registry-mirrors": ["https://自己的docker加速地址.mirror.aliyuncs.com"]
	}
	EOF
	sudo systemctl daemon-reload
	sudo systemctl restart docker
	```
4. 生成 kolla 密码

	```
	kolla-genpwd
	```
5. 执行 precheck

	```
	kolla-ansible prechecks
	```
6. 执行 pull（可以不执行，deploy 的时候会自动 pull）

	```
	kolla-ansible pull
	```
7. 执行deploy

	```
	kolla-ansible deploy
	```

# 使用 openstack
1. 安装openstack client

	```
	pip install python-openstackclient -i https://pypi.tuna.tsinghua.edu.cn/simple
	```
2. 生成admin-rc文件

	```
	kolla-ansible post-deploy
	默认是生成的文件名是: /etc/kolla/admin-openrc.sh
	```

3. 测试openstack环境

	```
	source  /etc/kolla/admin-openrc.sh
	/usr/share/kolla-ansible/init-runonce
	```



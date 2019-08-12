# Build Openstack Lab Environment

## Prepare

1. Topo 结构图

	![](img/openstack-env-architecture.png)

1. 配置 SSH 客户端

		Host training-01
		    HostName        training-01.maodouzi.net
		    User            root
		    IdentityFile    ~/.ssh/id_rsa_openstack

		Host training-01_aio
		    HostName        training-01.maodouzi.net
		    Port            8600
		    User            root
		    IdentityFile    ~/.ssh/id_rsa_openstack

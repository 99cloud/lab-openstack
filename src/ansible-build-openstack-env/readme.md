# lab-ansible

## Prepare

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

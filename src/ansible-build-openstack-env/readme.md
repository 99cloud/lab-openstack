# lab-ansible

## Prepare

1. 配置 SSH 客户端

		Host training-16
		    HostName        training-16.maodouzi.net
		    User            root
		    IdentityFile    ~/.ssh/id_rsa_openshift

		Host training-16_aio
		    HostName        training-16.maodouzi.net
		    Port            8600
		    User            root
		    IdentityFile    ~/.ssh/id_rsa_openshift

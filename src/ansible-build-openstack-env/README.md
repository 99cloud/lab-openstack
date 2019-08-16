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

1. kolla-aio lab 环境安装步骤：
    1. 笔记本上，初始化宿主机环境，以及安装前准备

            ansible-playbook -i kolla-aio-training-01.yml playbooks/kolla-aio-init.yml

    1. 登陆 training-01_aio 机器，安装 openstack

            kolla-ansible prechecks && kolla-ansible deploy

    1. 笔记本上，安装后配置

            ansible-playbook -i kolla-aio-training-01.yml playbooks/kolla-aio-post.yml

    1. 登陆 training-01_aio 机器，初始化 openstack

            /usr/share/kolla-ansible/init-runonce

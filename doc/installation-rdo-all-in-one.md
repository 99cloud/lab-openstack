# rdo介绍

1. 在开发测试环境中，部署一个kolla的allinone环境，需要花费很长时间，如果不是为了跑虚拟机，那么没必要花大量时间来部署kolla。
2. 测试的时候推荐使用rdo来部署allinone节点。
3. [rdo参考链接](https://www.rdoproject.org/install/packstack/)

# rdo部署条件

1. centos 操作系统能够访问互联网
2. 关闭selinux和firewalld
3. 硬件满足4C/8G/40G //最好16G内存
4. 如果开启cinder的LVM后端，需要添加一块磁盘并且创建cinder-volumes组

# rdo部署

1. 设置语言

    ```
    LANG=en_US.utf-8
    LC_ALL=en_US.utf-8
    ```
2. 停止服务

    ```
    sudo systemctl disable firewalld
    sudo systemctl stop firewalld
    sudo systemctl disable NetworkManager
    sudo systemctl stop NetworkManager
    sudo systemctl enable network
    sudo systemctl start network
    ```
3. 安装相关软件包

    ```
    sudo yum install -y centos-release-openstack-stein
    ```
4. 确保仓库可用

    ```
    yum install yum-utils -y
    yum-config-manager --enable openstack-stein
    ```
5. 更新系统rpm包

    ```
    sudo yum update -y
    ```
6. 安装Packstack

    ```
    sudo yum install -y openstack-packstack
    ```
7. 生成answer-file

    ```
    packstack --gen-answer-file=./answer-file
    ```
8.  根据自己需求修改answer-file，开启或者关闭其中的服务（可选）

   ```
   vi answer-file
   CONFIG_NEUTRON_OVS_BRIDGE_IFACES=br-ex:eth1
   其他的看说明即可
   ```
9. 部署allinone

    * 如果上一步没有生成answer-file，全部使用默认，则执行

        ```
        sudo packstack --allinone
        ```
    * 否则，直接使用自己修改的anser-file

        ```
        sudo packstack  --answer-file answer-file
        ```

# 部署后使用

1. 访问地址 http://$YOURIP/dashboard，用户名admin，密码在/root/keystonerc_admin中。


# 删除allinone环境

1. 把如下命令放到文件中，并且执行。

    ```
    # Warning! Dangerous step! Destroys VMs
    for x in $(virsh list --all | grep instance- | awk '{print $2}') ; do
    virsh destroy $x ;
    virsh undefine $x ;
    done ;
    # Warning! Dangerous step! Removes lots of packages, including many
    # which may be unrelated to RDO.
    yum remove -y nrpe "*nagios*" puppet ntp ntp-perl ntpdate "*openstack*" \
    "*nova*" "*keystone*" "*glance*" "*cinder*" "*swift*" \
    mysql mysql-server httpd "*memcache*" scsi-target-utils \
    iscsi-initiator-utils perl-DBI perl-DBD-MySQL ;
    ps -ef | grep -i repli | grep swift | awk '{print $2}' | xargs kill ;
    # Warning! Dangerous step! Deletes local application data
    rm -rf /etc/nagios /etc/yum.repos.d/packstack_* /root/.my.cnf \
    /var/lib/mysql/ /var/lib/glance /var/lib/nova /etc/nova /etc/swift \
    /srv/node/device*/* /var/lib/cinder/ /etc/rsync.d/frag* \
    /var/cache/swift /var/log/keystone ;
    umount /srv/node/device* ;
    killall -9 dnsmasq tgtd httpd ;
    setenforce 1 ;
    vgremove -f cinder-volumes ;
    losetup -a | sed -e 's/:.*//g' | xargs losetup -d ;
    find /etc/pki/tls -name "ssl_ps*" | xargs rm -rf ;
    for x in $(df | grep "/lib/" | sed -e 's/.* //g') ; do
    umount $x ;
    done
    ```

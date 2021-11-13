# DevStack AIO Wallaby 本地环境搭建步骤

1. MacOS / VMWare Fusion 15，或者 Linux KVM
1. 6Core / 16G 内存 / 30G 硬盘 1 块 / NAT 网络单张网卡 / 对虚拟机打开 VT 允许嵌套虚拟化
1. Ubuntu 20.04 Server ISO，安装系统，配置 SSH 密钥登陆，关机，打快照
1. [可选] 配置 Ubuntu [apt 清华源](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)
1. `apt-get update -y && apt-get upgrade -y`
1. [DevStack 单机版本官方文档](https://docs.openstack.org/devstack/latest/guides/single-machine.html)，当前最新的稳定版本是 Victoria。注意各版本的 devstack 都只保证兼容其发布时间节点上的最近两个的 Linux 主流 LTS 发行版本。或者参考这个[官方文档](https://docs.openstack.org/devstack/latest/)。
1. 创建 stack 用户

    ```bash
    sudo useradd -s /bin/bash -d /opt/stack -m stack
    echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
    sudo -u stack -i
    ```

1. 配置 pip 豆瓣源

    只需在用户 stack 家目录中 .pip 目录内创建 pip.conf 配置文件，以使用阿里云为例，配置文件内容如下

    ```ini
    [global]
    index-url = http://mirrors.aliyun.com/pypi/simple/
    [install]
    trusted-host=mirrors.aliyun.com
    ```

1. 如果每次执行 sudo 都很慢的话，需要把你的主机名加到 `/etc/hosts`，类似：`127.0.0.1 yourhostname`，参考：[Terminal command with sudo takes a long time](https://askubuntu.com/questions/322514/terminal-command-with-sudo-takes-a-long-time)。
1. 下载 Wallaby 版 Devstack 源码

    ```bash
    # stack 用户，cd 到 stack 用户 home 目录，默认是 /opt/stack
    git clone -b stable/wallaby http://git.trystack.cn/cgit/openstack/devstack
    cd devstack
    ```

1. 提前下载一些在安装过程中需要用到的大文件
    - 从 [github](https://github.com/etcd-io/etcd/releases/download/v3.3.12/etcd-v3.3.12-linux-amd64.tar.gz) 下载 `etcd-v3.3.12-linux-amd64.tar.gz` 下了一小时，可以提前下好从 [华为镜像](https://mirrors.huaweicloud.com/etcd/v3.3.12/etcd-v3.3.12-linux-amd64.tar.gz) 提前下好放到：`/opt/stack/devstack/files/etcd-v3.3.12-linux-amd64.tar.gz`

        ```bash
        cd /opt/stack/devstack/files/
        wget https://mirrors.huaweicloud.com/etcd/v3.3.12/etcd-v3.3.12-linux-amd64.tar.gz
        ```

    - 从 github 或者其它镜像网站下载 cirros-0.5.2-x86_64-disk.img 放到 /opt/stack/devstack/files/ 下面，Wallaby 版本默认用这个

        ```bash
        cd /opt/stack/devstack/files/
        wget https://github.com/cirros-dev/cirros/releases/download/0.5.2/cirros-0.5.2-x86_64-disk.img
        ```

1. 复制和修改 samples/local.conf 文件，如下配置是使用 wallaby 版本，安装 heat

    ```diff
    28,30c28,30
    < ADMIN_PASSWORD=secret
    < DATABASE_PASSWORD=$ADMIN_PASSWORD
    < RABBIT_PASSWORD=$ADMIN_PASSWORD
    ---
    > ADMIN_PASSWORD=nomoresecret
    > DATABASE_PASSWORD=stackdb
    > RABBIT_PASSWORD=stackqueue
    32,39d31
    <
    < GIT_BASE=http://git.trystack.cn
    < NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
    < SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git
    < enable_service s-proxy s-object s-container s-account h-eng h-api h-api-cfn h- api-cw q-svc q-dhcp q-meta q-agt q-l3 c-bak n-spice
    <
    < enable_plugin heat http://git.trystack.cn/openstack/heat stable/wallaby
    < enable_plugin heat-dashboard http://git.trystack.cn/openstack/heat-dashboard stable/wallaby
    ```

    ```console
    stack@devstack-aio:~/devstack$ cat local.conf | grep -v ^# | grep -v ^$
    [[local|localrc]]
    ADMIN_PASSWORD=secret
    DATABASE_PASSWORD=$ADMIN_PASSWORD
    RABBIT_PASSWORD=$ADMIN_PASSWORD
    SERVICE_PASSWORD=$ADMIN_PASSWORD
    GIT_BASE=http://git.trystack.cn
    NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
    SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git
    enable_service s-proxy s-object s-container s-account h-eng h-api h-api-cfn h- api-cw q-svc q-dhcp q-meta q-agt q-l3 c-bak n-spice
    enable_plugin heat http://git.trystack.cn/openstack/heat stable/wallaby
    enable_plugin heat-dashboard http://git.trystack.cn/openstack/heat-dashboard stable/wallaby
    LOGFILE=$DEST/logs/stack.sh.log
    LOGDAYS=2
    SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5
    SWIFT_REPLICAS=1
    SWIFT_DATA_DIR=$DEST/data
    ```

1. [可选] 创建 Volume Group，[参考](https://developer.aliyun.com/article/311612)

    ```bash
    pvcreate /dev/sdb

    # 如果找不到，是Linux 的 lvm 默认配置不允许在 /dev/sdb 上创建 PV，需要将 sdb 添加到 /etc/lvm.conf 的 filter 中
    global_filter = ["a|sdb|", ...]
    ```

1. 关机，打快照，开机
1. 开始安装 & 等待安装完成，安装完成后（ 正常的网络基本能稳定在 2500 秒以内，大约 40 分钟左右完成 ）关机，打快照

    ```bash
    ./stack.sh
    ```

1. Devstack 的安装日志在：`/opt/stack/logs`，可以用来分析哪里报错，以及哪一步慢。
1. 如何判断当前 devstack 安装出来的 openstack 的版本和对应的 python 解释器的版本？可以 ps -ef | grep python 找到各个服务的进程，然后看对应的 python 解释器的版本 python --version，以及看服务源码的版本：git status

    ```console
    $ ps -ef | grep swift
    stack    111224      1  2 00:53 ?        00:00:21 /usr/bin/python3.6 /usr/local/bin/swift-object-server /etc/swift/object-server/1.conf -v
    stack    112380 111853  0 00:53 ?        00:00:00 /usr/bin/python3.6 /usr/local/bin/swift-container-server /etc/swift/container-server/1.conf -v

    stack@u1804:~/glance$ git status
    On branch stable/victoria
    Your branch is up to date with 'origin/stable/victoria'.

    nothing to commit, working tree clean
    ```

# DevStack AIO Vultr 环境搭建步骤

1. 选 20.04
1. 参考 <https://stackoverflow.com/questions/63439723/error-in-installation-of-openstack-in-ubuntu>

    ```bash
    apt-get update
    apt-get upgrade
    apt-get install iptables
    apt-get install arptables
    apt-get install ebtables

    update-alternatives --set iptables /usr/sbin/iptables-legacy || true
    update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy || true
    update-alternatives --set arptables /usr/sbin/arptables-legacy || true
    update-alternatives --set ebtables /usr/sbin/ebtables-legacy || true
    ```

1. 改配置文件 local.conf

    ```bash
    stack@coalab001:~/devstack$ cat local.conf | grep -v '^$' | grep -v '^#'
    [[local|localrc]]
    ADMIN_PASSWORD=trystack99cloud
    DATABASE_PASSWORD=$ADMIN_PASSWORD
    RABBIT_PASSWORD=$ADMIN_PASSWORD
    SERVICE_PASSWORD=$ADMIN_PASSWORD
    enable_service s-proxy s-object s-container s-account h-eng h-api h-api-cfn h- api-cw q-svc q-dhcp q-meta q-agt q-l3 c-bak n-spice
    enable_plugin heat https://git.openstack.org/openstack/heat stable/wallaby
    enable_plugin heat-dashboard https://git.openstack.org/openstack/heat-dashboard stable/wallaby
    LOGFILE=$DEST/logs/stack.sh.log
    LOGDAYS=2
    SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5
    SWIFT_REPLICAS=1
    SWIFT_DATA_DIR=$DEST/data
    ```

1. 创建 pv：`pvcreate /dev/sdb`
1. 然后可以开始：`./unstack.sh && ./statck.sh`

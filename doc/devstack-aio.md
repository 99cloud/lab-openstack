# DevStack AIO 环境搭建步骤

1. MacOS / VMWare Fusion 15
1. 6Core / 16G 内存 / 40G 硬盘 2 块 / NAT 网络单张网卡 / 对虚拟机打开 VT 允许嵌套虚拟化
1. Ubuntu 20.04 Server ISO，安装系统，配置 SSH 密钥登陆，关机，打快照
1. 配置 Ubuntu [apt 清华源](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)，apt-get update && apt-get upgrade
1. 配置 pip 豆瓣源，其它源（ 比如阿里、清华、中科大 ）更新速度稍慢，比如 os-brick===3.2.0 会找不到，最多 3.1.0。如果你发现 pip 速度不慢，就不要配置这里，因为 wallaby 时，豆瓣源对 tempest 的 oslo.log 的高版本无法下载到。

    ```console
    $ sudo touch /etc/pip.conf
    
    $ sudo cat /etc/pip.conf
    [global]
    index-url = https://pypi.douban.com/simple/
    ```

    **注意：20.04 在 /etc/pip.conf 配置不生效，可能是因为 20.04 上没有 pip 命令，必须 python -m pip，未深究。可以在 stack / root 的 home 目录下创建 ~/.pip/pip.conf，可以生效。**

1. 如果每次执行 sudo 都很慢的话，需要把你的主机名加到 `/etc/hosts`，类似：`127.0.0.1 yourhostname`，参考：[Terminal command with sudo takes a long time](https://askubuntu.com/questions/322514/terminal-command-with-sudo-takes-a-long-time)
1. [DevStack 单机版本官方文档](https://docs.openstack.org/devstack/latest/guides/single-machine.html)，当前最新的稳定版本是 Victoria。注意各版本的 devstack 都只保证兼容其发布时间节点上的最近两个的 Linux 主流 LTS 发行版本。或者参考这个[官方文档](https://docs.openstack.org/devstack/latest/)，类似的。

    ```bash
    sudo useradd -s /bin/bash -d /opt/stack -m stack
    
    sudo su
    apt-get install sudo -y || yum install -y sudo
    echo "stack ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
    exit
    
    sudo su - stack
    
    sudo apt-get install git -y || sudo yum install -y git
    git clone http://git.trystack.cn/openstack/devstack.git
    cd devstack

    ```

1. 提前下载一些在安装过程中需要用到的大文件
    - 从 [github](https://github.com/etcd-io/etcd/releases/download/v3.3.12/etcd-v3.3.12-linux-amd64.tar.gz) 下载 `etcd-v3.3.12-linux-amd64.tar.gz` 下了一小时，可以提前下好从 [华为镜像](https://mirrors.huaweicloud.com/etcd/v3.3.12/etcd-v3.3.12-linux-amd64.tar.gz) 提前下好放到：`/opt/stack/devstack/files/etcd-v3.3.12-linux-amd64.tar.gz`

        ```bash
        cd /opt/stack/devstack/files/
        wget https://mirrors.huaweicloud.com/etcd/v3.3.12/etcd-v3.3.12-linux-amd64.tar.gz
        ```

    - 从 [github](https://github.com/cirros-dev/cirros/releases/download/0.5.1/cirros-0.5.1-x86_64-disk.img) 或者其它镜像网站下载 `cirros-0.5.1-x86_64-disk.img` 放到 `/opt/stack/devstack/files/` 下面，Victoria 版本默认用这个
    - 从 [github](https://github.com/cirros-dev/cirros/releases/download/0.4.0/cirros-0.4.0-x86_64-disk.img) 或者其它镜像网站下载 `cirros-0.4.0-x86_64-disk.img` 放到 `/opt/stack/devstack/files/` 下面，Ussuri 版本默认用这个
    - 从 [bootstrap.pypa.io](https://bootstrap.pypa.io/get-pip.py) 下载 `get-pip.py` 放到：`/opt/stack/devstack/files/`
    
1. 复制和修改 samples/local.conf 文件，如下配置是使用最新版本，使用默认配置，不安装 heat
  
    ```console
    $ cp samples/local.conf .
    
    # 编辑复制过来的 local.conf 文件
    
    $ diff local.conf samples/local.conf 
    28,30c28,30
    < ADMIN_PASSWORD=trystack
    < DATABASE_PASSWORD=$ADMIN_PASSWORD
    < RABBIT_PASSWORD=$ADMIN_PASSWORD
    ---
    > ADMIN_PASSWORD=nomoresecret
    > DATABASE_PASSWORD=stackdb
    > RABBIT_PASSWORD=stackqueue
    32,33d31
    < 
    < GIT_BASE=http://git.trystack.cn
    < NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
    < SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git

    $ cat local.conf | grep -v ^# | grep -v ^$
    [[local|localrc]]
    ADMIN_PASSWORD=trystack
    DATABASE_PASSWORD=$ADMIN_PASSWORD
    RABBIT_PASSWORD=$ADMIN_PASSWORD
    SERVICE_PASSWORD=$ADMIN_PASSWORD
    GIT_BASE=http://git.trystack.cn
    NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
    SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git
    LOGFILE=$DEST/logs/stack.sh.log
    LOGDAYS=2
    SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5
    SWIFT_REPLICAS=1
    SWIFT_DATA_DIR=$DEST/data
    ```

1. 如果需要用 stable/victoria 版本，启用 swift & heat，操作和配置如下

    ```console
    stack@u1804:~/devstack$ git checkout stable/victoria
    Branch 'stable/victoria' set up to track remote branch 'stable/victoria' from 'origin'.
    Switched to a new branch 'stable/victoria'

    stack@u1804:~/devstack$ diff local.conf samples/local.conf 
    28,30c28,30
    < ADMIN_PASSWORD=trystack
    < DATABASE_PASSWORD=$ADMIN_PASSWORD
    < RABBIT_PASSWORD=$ADMIN_PASSWORD
    ---
    > ADMIN_PASSWORD=nomoresecret
    > DATABASE_PASSWORD=stackdb
    > RABBIT_PASSWORD=stackqueue
    32,38d31
    < 
    < GIT_BASE=http://git.trystack.cn
    < NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
    < SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git
    < 
    < enable_service s-proxy s-object s-container s-account h-eng h-api h-api-cfn h- api-cw q-svc q-dhcp q-meta q-agt q-l3 c-bak n-spice
    < enable_plugin heat http://git.trystack.cn/openstack/heat stable/victoria
    < enable_plugin heat-dashboard http://git.trystack.cn/openstack/heat-dashboard stable/victoria

    stack@u1804:~/devstack$ cat local.conf | grep -v ^# | grep -v ^$
    [[local|localrc]]
    ADMIN_PASSWORD=trystack
    DATABASE_PASSWORD=$ADMIN_PASSWORD
    RABBIT_PASSWORD=$ADMIN_PASSWORD
    SERVICE_PASSWORD=$ADMIN_PASSWORD
    GIT_BASE=http://git.trystack.cn
    NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
    SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git
    enable_service s-proxy s-object s-container s-account h-eng h-api h-api-cfn h- api-cw q-svc q-dhcp q-meta q-agt q-l3 c-bak n-spice
    enable_plugin heat http://git.trystack.cn/openstack/heat stable/victoria
    enable_plugin heat-dashboard http://git.trystack.cn/openstack/heat-dashboard stable/victoria
    LOGFILE=$DEST/logs/stack.sh.log
    LOGDAYS=2
    SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5
    SWIFT_REPLICAS=1
    SWIFT_DATA_DIR=$DEST/data
    ```

1. 创建 Volume Group，[参考](https://developer.aliyun.com/article/311612)

    ```bash
    pvcreate /dev/sdb
    
    # 如果找不到，是Linux 的 lvm 默认配置不允许在 /dev/sdb 上创建 PV，需要将 sdb 添加到 /etc/lvm.conf 的 filter 中
    global_filter = ["a|sdb|", ...]
    ```

1. 指定 pip，wheels，setuptools 的版本，避免部署过程中遇到依赖不匹配的问题（wallaby 版本已经加上了 cap-pip.txt，应该不用改这步了，但没试过）
1. 取消检查 setuptools 版本是否与 requirements.txt 的匹配，由于 requirements.txt 每次都会 update 到最新的版本，使用旧版本不一定会通过检测

    ```console
    stack@u1804:~/devstack$ cp tools/install_pip.sh tools/install_pip_default.sh
    stack@u1804:~/devstack$ vi tools/install_pip.sh

    stack@u1804:~/devstack$ diff tools/install_pip.sh tools/install_pip_default.sh
    94c94
    <     sudo -H -E python${PYTHON3_VERSION} $LOCAL_PIP pip==20.2.4 wheel==0.30.0 setuptools==39.0.1
    ---
    >     sudo -H -E python${PYTHON3_VERSION} $LOCAL_PIP
    153c153
    < #pip_install_gr setuptools
    ---
    > pip_install_gr setuptools
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

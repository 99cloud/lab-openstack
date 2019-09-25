# exam-openstack

## 选择题（ 8 分/题，共 10 题 ）

1. 在 centos7 系统中如果无法用 yum 安装 ansible，那么可以用（  ）命令安装ansible。  

    ```text
    A. apt install ansible
    B. apt-get install ansible
    C. pip3 install ansible
    D. brew install ansible
    ```

2. 部署ansible时需要免密登录其他节点，生成ssh密钥文件的命令是（  ）。  

    ```text
    A. sshkey-gen  
    B. sshgen-prikey  
    C. gen-sshkey  
    D. ssh-keygen  
    ```

3. pip 使用本地源（ 假设本地源的 url 是`https://pypi.tuna.tsinghua.edu.cn/simple` ），在命令行中使用这个地址加速的完全命令是（ ）。  

    ```text
    A. pip install ansible -i https://pypi.tuna.tsinghua.edu.cn/simple
    B. pip install ansible -u https://pypi.tuna.tsinghua.edu.cn/simple
    C. pip install ansible --url https://pypi.tuna.tsinghua.edu.cn/simple
    B. pip install ansible --mirrors https://pypi.tuna.tsinghua.edu.cn/simple
    ```

4. kvm 查看当前系统中所有虚拟机的命令是（无论是否运行）（ ）。  

    ```text
    A. libvirt list --all
    B. virsh list --all
    C. virsh list-all
    D. libvirt allvms
    ```

5. kvm 删除一台名为node1的虚拟机，命令为（ ）。  

    ```text
    A. virsh delete node1
    B. virsh destroy node1
    C. virsh undefine node1
    D. virsh drop node1
    ```

6. 以下哪个不是网络监控工具（ ）？  

    ```text
    A. Postman
    B. Wireshark
    C. winscp
    D. Fiddler
    ```

7. 以下哪个不是自动化运维框架。  

    ```text
    A. Puppet
    B. Metasploit
    C. Ansible
    D. Saltstack
    ```

8. 发现 centos7 系统中没有 pip 或 pip3 命令，那我们应该用（ ）命令安装 pip / pip3。  

    ```text
    A. yum install -y python-pip
    B. yum install -y pip
    C. yum install -y pip-python
    D. yum install -y easyinstall
    ```

9. 通过 OpenStack API 直接获取主机列表时，我们需要先获取 token，如下哪条命令可用于获取 token ？

    ```text
    A. openstack token issue
    B. openstack token get
    C. openstack show token
    D. openstack token create
    ```

10. ansible playbook 的配置文件格式为 ？

    ```text
    A. yaml 和 ini
    B. xml 和 yml
    C. txt 和 ini
    D. ini 和 xml
    ```

## 填空题（ 4 分/题，共 5 空 ）

1. docker 的底层是 linux container，linux container 的 2 大基础是：`__________` 和 `__________` 
2. 在实验环境中，我们想用主机名来让各台机器相互通信，实现类似于dns的功能，这个文件是：`__________`
3. kolla-ansible 部署 openstack 时，各个服务的日志默认存储在：`__________`
4. 如果我们需要从 github 下载克隆代码，在 centos7 中我们需要使用 yum 安装：`________` 工具  

## 答案

1. 选择题答案

	```text
	01-05 C，D，A，B，C
	06-10 C，B，A，A，A
	```

2. 填空题答案（前 2 题的答案可以互换，大小写不敏感，后面也可以没有 s）

	```text
	1. Namespaces
	2. Cgroups
	3. /etc/hosts 
	4. /var/lib/docker/volumes/kolla_logs/_data/{project_name}
	5. git
	```
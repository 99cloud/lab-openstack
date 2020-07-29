# lab-openstack

## Catalog

| Date | Time | Title | Content |
| ---- | ---- | ----- | ------- |
| 第 1 天 | 上午 | [lab-00 Prerequisites](#lab-00-prerequisites--catalog-) | [SSH Tools](#ssh-tools--catalog-) |
| | | | [KVM Commands](#kvm-commands--catalog-) |
| | | [lab-01 OpenStack API](#lab-01-openstack-api--catalog-) | [API Quick Start](#api-quick-start--catalog-) |
| | | | [API Design](#api-design--catalog-) |
| | 下午 | | [Network Monitor Tools](#network-monitor-tools--catalog-) |
| | | [lab-02 Automation Frameworks](#lab-02-automation-frameworks--catalog-) | [Fabric Quick Start](#fabric-quick-start--catalog-) |
| | | | [Fabric in Details](#fabric-in-details--catalog-) |
| | | | [Ansible as a Plus](#ansible-as-a-plus--catalog-) |
| | | | [Ansible Common Concepts](#ansible-common-concepts--catalog-) |
| | | | [Ansible Common Modules](#ansible-common-modules--catalog-) |
| | | | [Ansible Demo](#ansible-demo--catalog-) |
| | | | [[Optional] AWX](#optional-awx--catalog-) |
| | | | [[Optional] Terraform](#optional-terraform--catalog-) |
| 第 2 天 | 上午 | [lab-03 OpenStack Ansible Provider](#lab-03-openstack-ansible-provider--catalog-) | [Ansible Cloud Provider](#ansible-cloud-provider--catalog-) |
| | | | [OpenStack Ansible Provider](#openstack-ansible-provider--catalog-) |
| | | [lab-04 OpenStack kolla-ansible](#lab-04-openstack-kolla-ansible--catalog-) | [Docker Quick Start](#docker-quick-start--catalog-) |
| | 下午 | | [Debug in Docker Container](#debug-in-docker-container--catalog-) |
| | | | [Kolla-Ansible Quick Start](#kolla-ansible-quick-start--catalog-) |
| | | | [Kolla-Ansible Installation & Maintenance](#kolla-ansible-installation--maintenance--catalog-) |
| | | [lab-05 OpenStack Debug](#lab-05-openstack-debug--catalog-) | [Debug with DevStack](#debug-with-devstack--catalog-) |
| | | | [Debug with Kolla-Ansible](#debug-with-kolla-ansible--catalog-) |
| | | | [[Optional] RDO](#optional-rdo--catalog-) |

## lab-00 Prerequisites ( [Catalog](#catalog) )

### SSH Tools ( [Catalog](#catalog) )

1. Target Machine

    ```bash
    ssh root@training-01.demotheworld.com
    # ...
    ssh root@training-15.demotheworld.com
    ```

1. [Putty](https://www.putty.org/) Config
    - Text font
    - Console log line number
    - Login user
    - [Optional]: Private cert
1. Questions
    1. Config Putty client, to connect to lab target hosts
    1. [Optional]: Connect to lab target hosts without type the password
    1. `http://training-15.demotheworld.com`

### KVM Commands ( [Catalog](#catalog) )

1. List all vms

    ```bash
    virsh list --all
    ```

1. List a specific vm's snaphosts

    ```bash
    virsh snapshot-list <vm_name>
    virsh snapshot-list kolla-aio
    ```

1. Revert a vm by a specific snapshots

    ```bash
    virsh snapshot-revert <vm_name> --snapshotname <snapshot_name>
    virsh snapshot-revert kolla-aio --snapshotname kolla-aio.common_aio
    ```

1. Delete a vm by a specific snapshots with its name

    ```bash
    virsh snapshot-delete <vm_name> --snapshotname <snapshot_name>
    virsh snapshot-delete kolla-aio --snapshotname kolla-aio.common_aio
    ```

1. [Attention][Do not run]: Remove a vm

    ```bash
    # Destroy a vm
    virsh destroy <vm_name>
    virsh destroy kolla-aio

    # Clear a specific vm's all snapshots
    virsh snapshot-list <vm_name> | awk '{print $1}' | xargs -i virsh snapshot-delete <vm_name> --snapshotname {}
    virsh snapshot-list kolla-aio | awk '{print $1}' | xargs -i virsh snapshot-delete kolla-aio --snapshotname {}

    # Remove a vm
    virsh undefine <vm_name>
    virsh undefine kolla-aio
    ```

1. Questions
    1. Create a snaphost for test
    1. Revert vm instances by a specific snapshot
    1. Delete the test snapshot

## lab-01 OpenStack API ( [Catalog](#catalog) )

### API Quick Start ( [Catalog](#catalog) )

1. [OpenStack CLI Overview](https://docs.openstack.org/newton/user-guide/common/cli-overview.html)
    - [Install the OpenStack command-line clients](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)

        ```bash
        # Intall python-pip: Red Hat Enterprise Linux, CentOS, or Fedora
        yum install python36 python36-devel python36-pip gcc openssl-devel -y

        # Install openstack-client
        pip3 install python-openstackclient
        ```

    - [Set environment variables using the OpenStack RC file](https://docs.openstack.org/newton/user-guide/common/cli-set-environment-variables-using-openstack-rc.html)

        ```bash
        export OS_USERNAME=username
        export OS_PASSWORD=password
        export OS_TENANT_NAME=projectName
        export OS_AUTH_URL=https://identityHost:portNumber/v2.0
        # The following lines can be omitted
        export OS_TENANT_ID=tenantIDString
        export OS_REGION_NAME=regionName
        export OS_CACERT=/path/to/cacertFile
        ```

    - [Demo]: Config OpenStack client environment

        ```bash
        ssh kolla-aio "cat /etc/kolla/admin-openrc.sh"
        vi ~/.bash_profile
        . ~/.bash_profile
        ```

    - [Demo]: List endpoints

        ```bash
        openstack endpoint list
        ```

    - Questions
        - Create a server instance in Horizon dashboard
        - List vm instances: `openstack server list`
1. API vs CLI
    - [Demo]: Show CLI's backend requests

        ```bash
        openstack endpoint list -v --debug
        ```

    - [Demo]: TcpDump examples

        ```bash
        yum install tcpdump -y
        man tcpdump | less -Ip examples

        # TCP
        tcpdump -i br-mgt -s 0 -A 'tcp'

        # HTTP GET
        tcpdump -i br-mgt -s 0 -A 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'

        # HTTP POST
        tcpdump -i br-mgt -s 0 -A 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x504f5354'

        # HTTP Response Head & Data
        tcpdump -i br-mgt -s 0 -A '(((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
        tcpdump -i br-mgt -s 0 -X '(((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
        ```

### API Design ( [Catalog](#catalog) )

1. [Authentication](https://docs.openstack.org/api-ref/identity/v3/), [stein version](https://docs.openstack.org/keystone/stein/api_curl_examples.html)
    - [Demo]: Get unscope token

        ```bash
        curl -i \
          -H "Content-Type: application/json" \
          -d '
        { "auth": {
            "identity": {
              "methods": ["password"],
              "password": {
                "user": {
                  "name": "admin",
                  "domain": { "id": "default" },
                  "password": "UJCcUExoRddRtPC9LIyzzceDM2nHdjMIfwICZRsY"
                }
              }
            }
          }
        }' \
          "http://172.25.0.100:35357/v3/auth/tokens"
        ```

    - [Demo]: Get endpoint list with scope token

        ```bash
        TOKEN=$(openstack token issue | grep -E '^\|\s*id\s+' | awk '{print $4}')
        curl -s -H "X-Auth-Token: ${TOKEN}" http://172.25.0.100:5000/v3/endpoints | python -m json.tool
        ```

    - Questions
        - Issue a project scope token by CURL tool
        - Use this token to list endpoints

1. [Compute](https://docs.openstack.org/api-ref/compute/)
    - [Demo]: List servers

        ```console
        [root@openstack ~]# curl -s -H "X-Auth-Token: ${TOKEN}" http://172.25.0.100:8774/v2.1/ed009b94405443b393a132bb75ae1de8/servers | python -m json.tool
        #http://172.25.0.100:8774/v2.1/ is your nova endponit
        #ed009b94405443b393a132bb75ae1de8 is your project id
        ```

    - [Demo]: Launch a new server

        ```bash
        curl -X POST \
          http://172.25.0.100:8774/v2.1/f3816430aded4dbd92b3faeda1a87e0b/servers \
          -H 'Content-Type: application/json' \
          -H "X-Auth-Token: ${TOKEN}" \
          -d '{
            "server" : {
                "accessIPv4": "1.2.3.4",
                "accessIPv6": "80fe::",
                "name" : "new-server-test",
                "imageRef" : "eb901df6-801f-466f-8983-b55454b17cf5",
                "flavorRef" : "8ffeec2e-fc2d-496a-af53-5020849d630a",
                "networks" : [{
                    "uuid" : "0f2d90bc-da6d-4a0d-867e-e1a204e11f9f"
                }],
                "security_groups": [
                    {
                        "name": "default"
                    }
                ]
            }
        }'
        ```

1. [Block Storage](https://docs.openstack.org/api-ref/block-storage/v3/index.html)
    - [Demo]: Create a block storage

        ```bash
        curl -X POST \
          http://172.25.0.100:8776/v3/f3816430aded4dbd92b3faeda1a87e0b/volumes \
          -H 'Content-Type: application/json' \
          -H "X-Auth-Token: ${TOKEN}" \
          -d '{
            "volume": {
                "size": 10,
                "availability_zone": null,
                "source_volid": null,
                "description": "test volume",
                "multiattach": false,
                "snapshot_id": null,
                "backup_id": null,
                "name": null,
                "imageRef": null,
                "volume_type": null,
                "metadata": {},
                "consistencygroup_id": null
            }
        }'
        ```

    - [Demo]: Attach to a specific server instance

        ```bash
        curl -X POST \
          http://172.25.0.100:8776/v3/f3816430aded4dbd92b3faeda1a87e0b/volumes/07178089-7017-4d53-bb02-65b0a1b02bb5/action \
          -H 'Content-Type: application/json' \
          -H "X-Auth-Token: ${TOKEN}" \
          -d '{
            "os-attach": {
                "instance_uuid": "173d8d22-ce8e-4414-b286-008e33471d74",
                "mountpoint": "/dev/vdb"
            }
        }'
        ```

1. [Network](https://docs.openstack.org/api-ref/network/v2/index.html)
    - [Demo]: Create a network

        ```bash
        curl -X POST \
          http://172.25.0.100:9696/v2.0/networks \
          -H 'Content-Type: application/json' \
          -H "X-Auth-Token: ${TOKEN}" \
          -d '{
            "network": {
                "name": "sample_network",
                "admin_state_up": true,
                "mtu": 1400
            }
        }'
        ```

    - [Demo]: Create a subnet

        ```bash
        curl -X POST \
          http://172.25.0.100:9696/v2.0/subnets \
          -H 'Content-Type: application/json' \
          -H "X-Auth-Token: ${TOKEN}" \
          -d '{
            "subnet": {
                "network_id": "6f0b2c56-48ae-4981-89b2-bb5d1decb7ed",
                "ip_version": 4,
                "cidr": "192.168.199.0/24"
            }
        }'
        ```

    - Questions
        - Create a router

### Network Monitor Tools ( [Catalog](#catalog) )

1. Chrome Developer tools
    - [Demo]: Capture & Parse the HTTP requests

        ![chrome](../img/chrome1.png)

        ![chrome](../img/chrome2.png)

        ![chrome](../img/chrome3.png)
1. [Postman](https://www.getpostman.com/downloads/)
    - [Demo]: Send HTTP requests

        ![postman](../img/postman1.png)

        ![postman](../img/postman2.png)

        ![postman](../img/postman3.png)

        ![postman](../img/postman4.png)

        ![postman](../img/postman5.png)

        ```
        #head内容如下
        X-Auth-Toke: gAAAAABdQqoqaMFBasJV1p-mv9B0o3xQVCTdhGQDp3cBTuD2Wz0OJIA_xjmZG9XzTw7H7Za1dv-PAyacGe6StIkdrE1sj8P9C4fS0wTp9gDExt1m1QZ2RSj0im5OLwF0fX14VH7fiQvytS3D3aaMkQ

        # token 可以通过openstack token issue 获取
        # Content-Type是postman自动添加的
        # 请求地址如下
        POST http://10.211.55.100:9696/v2.0/routers

        # http://10.211.55.100:9696 为neutron的endpoint，可以通以openstack endpoint list获取
        # /v2.0/routers 是api接口 可以通过openstack网站上获取
        # 请求的body如下
        {
            "router": {
                "name": "router1",
                "external_gateway_info": {
                    "network_id"7c431bd4-985b-4a1a-ab21-166fa8",
                    "enable_snat": true
                },
                "admin_state_up": true
            }
        }

        # network_id 为provider网络的id，可以通过openstack network list 获取到
        # 其他的属性可以参考openstack的neutron api获取
        ```

1. [Fiddler](https://www.telerik.com/fiddler)
    - [Demo]: Collect trace
    - [Demo]: Play back
1. Windows 下的 OSI 七层模型的实现结构

    ```
              +-------------------------------+
              |           Ws2_32.dll          |
              +-------------------------------+
     User               |           |
              +-------------------------------+
              |           msafd.dll           |
              +-------------------------------+
                      |   System Call  |
                      | File Operation |
    ----------------------------------------------------------------------
                      |                |
              +-------------------------------+
              |           afd.sys             |
              |         \Device\Afd           |
              +-------------------------------+
     Kernel           | File Operation |
                      |      IRP       |
           +----------------------------------------+
           |                tcpip.sys               | ( Tdi layer )     --- 传输层
           | \Device\Tcp \Device\Udp \Device\RawIp  | ( Ndis Protocol ) --- 网络层
           +----------------------------------------+
                      |   Ndis lib     |
                      |                |
               +-------------------------------+
               |           k57xp32.sys         |      ( Miniport )      --- 链路层
               +-------------------------------+
               |       Net Interface Card      |                        --- 物理层
               +-------------------------------+
    ```

- 参考：[描述](http://blog.csdn.net/Henzox/article/details/38846117#)
	- 简单来讲，Windows 对网络部分的实现分为两部分，用户态部分和内核态部分。
		- 用户态部分为标准的`socket`调用，一般情况下可以认为有`ws2_32.dll`和`msafd.dll`组成，`msafd.dll`为一个服务提供者，主要完成`socket`用户层的代码实现
		- 在内核态`socket`的实现由`afd.sys`实现，它主要创建设备`\Device\Afd`来与`msafd.dll`进行交互，完成`socket`的创建等其它操作。
	- tcp/ip协议的传输层和网络层实现是在`tcpip.sys`里完成的，它主要完成两部分工作：传输层和网络层实现
		- 在传输层部分完成`TCP`,`UDP`,`RawIp`的绑定，连接等功能，主要服务于afd.sys发下来的`TDI`命令
		- 然后进入到网络层，来完成路由以及IP包的构成，网络层部分相当于一个Ndis协议驱动，一般来讲它会绑定所有的网卡来监听和发送IP包。
	- 链路层在笔者的电脑上是由`k57xp32.sys`驱动完成，不同的网卡此驱动可能不同，它相当于一个`Ndis Miniport`驱动，和Ndis协议驱动一样，都是运行在Ndis库营造的一个运行环境中，主要完成例如以内网数据包的构成，操作网卡发送数据包，以及注册中断接收数据包以及其它信息的工作。
	- 物理层，当然由网卡硬件来实现。
	- 有了上面清晰的结构之后，我们要开发一些业务就会非常明白的知道它工作在哪里
		- 比如TDI防火墙，就可以直接附加到`tcpip.sys`创建的几个命名设备对象上面，就可以监听到`afd.sys`发下来的TDI命令，进而可以拦截，一些`socket`创建，绑定，发送和接收的命令，从而完成防火墙的功能。当然，如果别人直接注册一个协议驱动，然后直接进行发包，那么这个防火墙就不能对这样的操作对待监控，比如直接发ARP包到局域网中，就可以造成攻击。但是如果你的防火墙工作在链表层上面，即注册一个中间层驱动来完成防火墙的功能，那么就又可以拦截掉我刚才假设的那种操作，所以如果一个Ndis中间层驱动来完成防火墙功能，那么就可以有更大的监控范围。
		- 再比如，想实现一个虚拟网卡，那么就可以完成一个Ndis小端口驱动，来让其它协议对你进行绑定，一些应用程序就可以直接选择这张网卡进行数据处理，便可完成一些特殊工作了。
- Netmon
	- ![Netmon-Layer.jpg](https://raw.githubusercontent.com/wu-wenxiang/Media-WebLink/master/qiniu/9e7c39ba1fa54c17b394a1918e4a0f3d-Netmon-Layer.jpg)
	- Netmon is between ndis and tcpip layer
	- TCP 包从APP到网卡最后发送之前，是需要经过几层：`NIC-ndis-tcpip-afd-userMode`
	- Application如果有杀毒软件，filter driver会load到其中的两个地方：`nic-ndis-<filter_driver>-tcpip-<filter_driver>-afd-userModeApp`
	- NDIS：Network Driver Interface Specification，这个是网卡的驱动接口。我们的netmom capture的包是从TCP/IP 到NDSI的，在某些情况下不能代表真正从NIC出去的包。
- Wireshark
	- 参考
		- [抓各种包](https://wiki.wireshark.org/CaptureSetup/)
		- Architecture
			- [WinPcap structure](https://www.winpcap.org/docs/docs_40_2/html/group__internals.html)
			- ![internals-arch.gif](https://raw.githubusercontent.com/wu-wenxiang/Media-WebLink/master/qiniu/37369909dc8d43308cb7d298bf998297-internals-arch.gif)
			- [Detail](https://www.winpcap.org/docs/iscc01-wpcap.pdf)
			- ![winpcap.png](https://raw.githubusercontent.com/wu-wenxiang/Media-WebLink/master/qiniu/37369909dc8d43308cb7d298bf998297-winpcap.png)
1. 操作：[Netmon](https://www.microsoft.com/en-us/download/details.aspx?id=4865) & [Wireshark](https://www.wireshark.org/download.html)
    - [Demo]: TCP handshake
    - [Demo]: TLS handshake
    - [Demo]: HTTP response data parser

## lab-02 Automation Frameworks ( [Catalog](#catalog) )

### Fabric Quick Start ( [Catalog](#catalog) )

1. Auto-Maintenance Frameworks
    - Ansible vs Others

        ![](../img/puppet-chef-ansible-saltstack.png)

    - Framework Differences

        ![](../img/auto-maintenance-difference.png)
1. SSH client configuration

    ```
    Host training-01
        HostName        training-01.maodouzi.net
        User            root
        IdentityFile    ~/.ssh/id_rsa_openstack

    Host training-01_aio
        HostName        training-01.maodouzi.net
        Port            8600
        User            root
        IdentityFile    ~/.ssh/id_rsa_openstack
    ```

1. SSH Proxy

    ```
    ProxyCommand    ssh fq -W %h:%p
    ProxyCommand    bash -c 'h=%h;ssh bastion -W ${h##prefix-}:%p'
    ```

1. Fabric Hello World

    ```console
    $ pip3 install fabric3

    $ cat fabricrc
    hosts = 172.25.0.200
    user = root
    password = 123456

    $ cat fabfile.py
    from fabric.api import run
    def hello():
        run("hostname")

    $ fab -c fabricrc hello
    [testhost] Executing task 'hello'
    [testhost] run: hostname
    [testhost] out: example.hostname.com
    Done.
    ```

### Fabric in Details ( [Catalog](#catalog) )

1. Fabric Concepts

    ![](../img/fabric-concepts.png)
1. Fabric Common Steps

    ![](../img/fabric-methods.png)

    ![](../img/fabric-steps.png)
1. [Demo]: [Deploy a website with Fabric](https://github.com/wu-wenxiang/Project-Python-Webdev/tree/master/u1604-fabric)

### Ansible as a Plus ( [Catalog](#catalog) )

1. Ansible Architecture

    ![](../img/ansible-architecture.png)
1. Ansible Hello World

    ```console
    pip3 install ansible==2.7.11

    $ cat /etc/ansible/hosts
    [testservers]
    test1
    test2

    ansible localhost -m ping
    ansible testservers -m ping

    ansible testservers -m shell -a "echo hello world"
    ```

1. Idempotency

### Ansible Common Concepts ( [Catalog](#catalog) )

1. Inventory ( ini )
1. Playbook ( yaml ) - Python data structure: number / string / list / dict
1. Role
1. Variables ( Global / Default )
1. Templates / Files
1. [Optional] Handler

### Ansible Common Modules ( [Catalog](#catalog) )

1. [ping](https://docs.ansible.com/ansible/latest/modules/ping_module.html)
1. [shell](https://docs.ansible.com/ansible/latest/modules/shell_module.html)
1. [template](https://docs.ansible.com/ansible/latest/modules/template_module.html)
1. [copy](https://docs.ansible.com/ansible/latest/modules/copy_module.html)
1. [cron](https://docs.ansible.com/ansible/latest/modules/cron_module.html)
1. [mount](https://docs.ansible.com/ansible/latest/modules/mount_module.html)
1. [service](https://docs.ansible.com/ansible/latest/modules/service_module.html)
1. [sysctl](https://docs.ansible.com/ansible/latest/modules/sysctl_module.html)
1. [user](https://docs.ansible.com/ansible/latest/modules/user_module.html)
1. [stat](https://docs.ansible.com/ansible/latest/modules/stat_module.html)
1. [get_url](https://docs.ansible.com/ansible/latest/modules/get_url_module.html)
1. [yum](https://docs.ansible.com/ansible/latest/modules/yum_module.html)/[apt](https://docs.ansible.com/ansible/latest/modules/apt_module.html)

### Ansible Demo ( [Catalog](#catalog) )

1. [Demo]: Template, copy files to target host with template

    ```console
    # cat config.ini.j2
    hosts = 172.25.0.200
    user = root
    password = {{ password }}

    # cat playbook.yml
    - hosts: testservers
      vars:
        password: "hello"
      tasks:
      - name: Create a DOS-style text file from a template
        template:
          src: /root/config.ini.j2
          dest: /root/config.ini

    # ansible-playbook -i /etc/ansible/hosts playbook.yml
    ```

1. [Demo]: [Deploy a website with Ansible](https://github.com/wu-wenxiang/Project-Python-Webdev/tree/master/u1604-ansible)
1. [Demo]: Deploy OpenShift

### [Optional] AWX ( [Catalog](#catalog) )

1. AWX & Tower

    ![](../img/ansible-awx.png)
1. AWX Hello World

### [Optional] Terraform ( [Catalog](#catalog) )

1. Terraform Hello World
    - [Demo]: OpenStack launch an instance

## lab-03 OpenStack Ansible Provider ( [Catalog](#catalog) )

### [Ansible Cloud Provider](https://docs.ansible.com/ansible/latest/modules/list_of_cloud_modules.html) ( [Catalog](#catalog) )

1. Azure
    - [Demo]: Register DNS in Azure

        ```console
        $ cat dns-sp.yml
        tenantId: "e967c2f0-fd97-47ce-89be-26cd63a261AA"
        subscriptionId: "d909fe64-bc51-4377-9907-29a63692cfAA"
        aadClientId: "97d30cbe-f7e3-4785-bdc2-dc6c4753a5AA"
        aadClientSecret: "27f60511-4680-4ff0-aadb-5202d6402aAA"
        resourceGroup: "openshift-dns"
        cloud: "AzureCloud"

        $ cat set-dns.yml
        - hosts: localhost
          tasks:
            - name: Get dns_yml
              include_vars:
                file: "dns-sp.yml"
                name: dns_sp
            - name: Dump dns_sp
              debug:
                msg: "{{ dns_sp }}"
            - name: Dump hosts
              debug:
                msg: "{{ item }}"
              loop: "{{ vultr_hosts }}"
            - name: Add Records to Azure Zone
              azure_rm_dnsrecordset:
                resource_group: "openshift-dns"
                relative_name: "{{ item.hostname }}"
                zone_name: "maodouzi.net"
                record_type: A
                state: present
                records:
                  - entry: "{{ item.ipaddr }}"
                cloud_environment: "{{ dns_sp.cloud }}"
                subscription_id: "{{ dns_sp.subscriptionId }}"
                client_id: "{{ dns_sp.aadClientId }}"
                secret: "{{ dns_sp.aadClientSecret }}"
                tenant: "{{ dns_sp.tenantId }}"
              loop: "{{ vultr_hosts }}"
          vars:
            - vultr_hosts:
              - {'hostname': 'training-01', 'ipaddr': '149.248.18.239'}
              - {'hostname': 'training-02', 'ipaddr': '8.6.8.15'}
              - {'hostname': 'training-03', 'ipaddr': '104.207.152.126'}
              - {'hostname': 'training-04', 'ipaddr': '144.202.127.252'}
              - {'hostname': 'training-05', 'ipaddr': '149.28.74.219'}
              - {'hostname': 'training-06', 'ipaddr': '45.77.120.38'}
              - {'hostname': 'training-07', 'ipaddr': '45.32.85.81'}
              - {'hostname': 'training-08', 'ipaddr': '207.246.99.128'}
              - {'hostname': 'training-09', 'ipaddr': '66.42.109.203'}
              - {'hostname': 'training-10', 'ipaddr': '149.28.78.167'}
              - {'hostname': 'training-11', 'ipaddr': '140.82.18.5'}
              - {'hostname': 'training-12', 'ipaddr': '66.42.105.38'}
              - {'hostname': 'training-13', 'ipaddr': '149.248.5.42'}
              - {'hostname': 'training-14', 'ipaddr': '45.63.60.228'}
              - {'hostname': 'training-15', 'ipaddr': '45.76.75.76'}
              - {'hostname': 'training-16', 'ipaddr': '45.32.64.92'}

        $ ansible-playbook set-dns.yml
        ```

    - [Demo]: Deploy openshift in Azure
1. [Optional] Aliyun

### OpenStack Ansible Provider ( [Catalog](#catalog) )

1. OpenStack Ansible Hello World
    - [Demo]: Get token

        ```yaml
        - hosts: localhost
          tasks:
            - name: Retrieve an auth token
              os_auth:
                auth:
                  auth_url: http://172.25.0.100:5000/v3
                  username: admin
                  project_name: admin
                  password: mo0xgPEqDDdWoYk2oxnlB60STu4MdFDNPXr0sUuh
                  user_domain_name: Default
                  project_domain_name: Default
            - name: Show auth token
              debug:
                var: auth_token
        ```

1. Compute
    - [Demo]: Create a server instance

        ```yaml
        - name: Create a server instance
          hosts: localhost
          tasks:
            - name: Launch a instance
              os_server:
                auth:
                  auth_url: http://172.25.0.100:5000/v3
                  username: admin
                  project_name: admin
                  password: mo0xgPEqDDdWoYk2oxnlB60STu4MdFDNPXr0sUuh
                  user_domain_name: Default
                  project_domain_name: Default
                state: present
                name: new-server-test
                image: 6cc537b7-dba4-4c2a-a25b-af19b6055979
                flavor: 1
                network: 1a657834-2bdc-4677-b513-aaf88f60a8cd
                security_groups: default
        ```

    - [Demo]: List server instance

        ```yaml
        - name: List server instance
          hosts: localhost
          tasks:
            - name: List server instance
              os_server_facts:
            - debug:
                var: openstack_servers
        ```

1. Block Storage
    - [Demo]: Create a block storage

        ```yaml
        - name: Create a block storage
          hosts: localhost
          tasks:
            - name: Create a volume
              os_volume:
                state: present
                size: 10
                display_name: "test volume"
        ```

1. Network
    - [Demo]: Create a network

        ```yaml
        - name: Create a network
            hosts: localhost
            tasks:
            - name: Create a network
              os_network:
                state: present
                name: sample_network
        ```

## lab-04 OpenStack kolla-ansible ( [Catalog](#catalog) )

### Docker Quick Start ( [Catalog](#catalog) )

1. Python Virtual Environment

    ```console
    # pip3 install virtualenv

    # virtualenv -p python3 .env
    Running virtualenv with interpreter /usr/bin/python3
    Already using interpreter /usr/bin/python3
    Using base prefix '/usr'
      No LICENSE.txt / LICENSE found in source
    New python executable in /root/.env/bin/python3
    Also creating executable in /root/.env/bin/python
    Installing setuptools, pip, wheel...
    done.

    # . .env/bin/activate
    (.env) [root@openstack-01 ~]# python
    Python 3.6.8 (default, Apr 25 2019, 21:02:35)
    [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> exit()
    ```

1. Docker Hello World
    - Quick Start

        ```console
        $ yum install docker -y
        $ systemctl start docker
        $ docker run hello-world

        $ docker run ubuntu:18.04 /bin/echo "Hello world"
        $ docker ps -a
        ```

    - Run Process in Docker

        ```console
        # stdin & terminal
        $ docker run -it ubuntu:18.04 /bin/bash
        $ ps -ef | grep bash
        ```

    - Backend Process in Docker

        ```console
        $ docker run -d ubuntu:18.04 /bin/sh -c "while true; do echo hello world; sleep 1; done"
        $ docker logs <container-id> -f
        $ docker exec -it <container-id> /bin/bash
        $ docker stop <container-id>
        ```

    - Python docker API

        ```console
        $ pip3 install docker

        $ python3
        Python 3.6.8 (default, Apr 25 2019, 21:02:35)
        [GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> import docker
        >>> client = docker.from_env()
        >>> print(client.containers.run("ubuntu:18.04", ["echo", "hello", "world"]))
        b'hello world\n'
        ```

    - [Ansible docker module](https://docs.ansible.com/ansible/latest/modules/docker_container_module.html)

        ```console
        $ cat docker.yml
        - name: Create a server instance
          hosts: localhost
          tasks:
            - name: Container present
              docker_container:
                name: mycontainer
                state: present
                image: ubuntu:18.04
                command: sleep infinity
            - name: Stop a container
              docker_container:
                name: mycontainer
                state: stopped

        $ ansible-playbook docker.yml
        ```

    - [Docker example](https://docs.docker.com/get-started/part2/)
1. Docker Concepts
    - Virtualization Evolution

        ![](../img/virtualization-evolution.svg)

    - Docker Underlying Tech

        ![](../img/docker-underlying-tech.png)

    - Linux Container Namespaces

        ![](../img/linux-container-namespaces.png)

    - Docker Architecture

        ![](../img/docker-architecture.png)

### Debug in Docker Container ( [Catalog](#catalog) )

1. View stdout history with the logs command.

    ```console
    $ docker run -d --name=logtest alpine /bin/sh -c "while true; do sleep 5; df -h; done"
    35f6353d2e47ab1f6c34073475014f4ab5e0b131043dca4454f67be9d8ef1253
    $ docker logs logtest
    Filesystem Size Used Available Use% Mounted on
    none 93.7G 2.0G 87.0G 2% /
    tmpfs 3.8G 0 3.8G 0% /dev
    tmpfs 3.8G 0 3.8G 0% /sys/fs/cgroup
    # ... etc ...
    ```

    - This history is available even after the container exits
    - as long as its file system is still present on disk (until it is removed with docker rm).
    - The data is stored in a json file buried under /var/lib/docker.
    - The log command takes options that allow you to follow this file, basically tail -f, as well as choose how many lines the command returns (tail -n).
1. Stream stdout with the attach command.
If you want to see what is written to stdout in real time then the attach command is your friend.

    ```console
    $ docker run -d --name=logtest alpine /bin/sh -c "while true; do sleep 5; df -h; done"
    26a329f1e7074f0c0f89caf266ad145ab427b1bcb35f82557e78bafe053faf44

    $ docker attach logtest
    Filesystem Size Used Available Use% Mounted on
    none 93.7G 2.0G 87.0G 2% /
    tmpfs 3.8G 0 3.8G 0% /dev
    tmpfs 3.8G 0 3.8G 0% /sys/fs/cgroup
    # … etc …
    Filesystem Size Used Available Use% Mounted on
    none 93.7G 2.0G 87.0G 2% /
    tmpfs 3.8G 0 3.8G 0% /dev
    tmpfs 3.8G 0 3.8G 0% /sys/fs/cgroup
    # … etc …
    ```

    - By default this command attaches stdin and proxies signals to the remote process. Options are available to control both of these behaviors.
    - To detach from the process use the default `ctrl-p ctrl-q` sequence.
    - If couldn't detach in this way, try kill :-)

        ```console
        # ps -ef | grep docker.*attach
        root     12224 10895  0 00:04 pts/2    00:00:00 /usr/bin/docker-current attach logtest3

        # kill -9 12224
        ```

1. Execute arbitrary commands with exec.
Maybe the most powerful all-around tool in your kit, the exec command allows you to run arbitrary commands inside a running container.

    ```console
    $ docker run -d --name=exectest alpine watch "echo 'This is a test.' >> /var/log/test.log"
    70ddfdf5169e755177a812959808973c92974dba2531c42a21ad9e50c8a4804c
    $ docker exec exectest cat /var/log/test.log
    This is a test.
    This is a test.
    This is a test.
    This is a test.

    # You can even use exec to get an interactive shell in the container.

    $ docker run -d --name=exectest alpine watch "echo 'This is a test.' >> /var/log/test.log"
    91e46bf5d19d4239a2f30af06669d4263580a01187d2290c33d7dee110f76356
    $ docker exec -it exectest /bin/sh
    / # ls -al /var/log
    total 12
    drwxr-xr-x 2 root root 4096 Mar 23 05:37 .
    drwxr-xr-x 10 root root 4096 Mar 23 05:37 ..
    -rw-r — r — 1 root root 192 Mar 23 05:38 test.log
    / # exit
    $
    ```

    - Note that exec only works while the container is running. So for a container that is crashing you’ll need to fall back on the logs command.
1. Override the ENTRYPOINT.
    - Every docker image has an entrypoint and command, whether defined in the dockerfile at build time or as an option to the docker run command at run time. The relationship between entrypoint and command can be a little confusing, and there are different ways to use them, but here is one setup that follows best practices and gives you a lot of customization ability.
    - Let’s say you are running a django app. First, you define the python process that runs the app as the entry point. This will make sure it is pid 1 inside the container. You can do this in the dockerfile.
    - `ENTRYPOINT ["python", "manage.py", "runserver"]`
    - You can also do it on the command line when docker run is called, and that is where the cool comes in. If the entry point is specified on the command line then it overrides any entry point set in the dockerfile when the image was built. This can be a powerful tool. Imagine a situation where the django image in this example was crashing due to a configuration problem. Instead of running manage.py you want to get a shell and poke around.
    - `docker run -d -p 80:80 --entrypoint /bin/sh /myrepo/mydjangoapp`
    - Now you can jump in, check the config, even try to run the manage.py command interactively to see what happens.
1. Add options with the CMD.
    - Back to that confusing relationship between ENTRYPOINT and CMD. Here’s one way to look at it: the ENTRYPOINT defines the process that runs as PID 1 in the container, and the CMD adds options to it.
    - If you don’t specify an ENTRYPOINT but you do specify a CMD then the implicit entrypoint is /bin/sh -c. CMD, like ENTRYPOINT, can be specified on the command line when docker run is called, which makes it another powerful tool for modifying container behavior. However, the usage is a little different.
    - `docker run -d -p 80:8000 /myrepo/mydjangoapp 0.0.0.0:8000`
    - Anything that appears after the image name in the docker run command is passed to the container and treated as CMD arguments, basically as if it were specified in the dockerfile like this:

        ```
        ENTRYPOINT ["python", "manage.py", "runserver"]
        CMD ["0.0.0.0:8000"]
        ```

    - Additional arguments can be passed as space-delimited parameters to the docker run call. This is a very convenient and flexible way to reconfigure an image for debugging purposes, by passing an option to increase log verbosity, for example.
    - 上述用于 K8S 时，yaml 用的是 command / args，[参考](https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/)

		```yaml
		apiVersion: v1
		kind: Pod
		metadata:
		  name: example
		  labels:
		    app: python
		  namespace: default
		spec:
		  containers:
		    - name: python
		      image: python
		      command: ["/bin/sh"]
		      args: ["-c", "while true; do echo hello; sleep 10;done"]
		      env:
		        - name: TZ
		          value: Asia/Shanghai
		```

1. Pause and unpause a container.
    - I doubt you’ll have use for this one very often, but it’s cool so I’m throwing it in here anyway. Using the docker pause command you can pause all of the processes inside a container.

        ```console
        $ docker run -d --name=pausetest alpine /bin/sh -c "while true; do sleep 2; date; done"
        e81e1bc519e4eb2e30a1c1e57198f0060147fa749ff8f93ba4f69bdf8a114311
        ```

    - The container is just echoing the date to stdout, so we can watch it with the attach command.

        ```console
        $ docker attach pausetest
        Wed Mar 23 06:21:40 UTC 2016
        Wed Mar 23 06:21:42 UTC 2016
        ```

    - Now pause the container, wait a bit, then unpause it.

        ```console
        $ docker pause pausetest
        pausetest
        $ docker unpause pausetest
        pausetest
        ```

    - And back in our other window where attach is running…

        ```console
        $ docker attach pausetest
        Wed Mar 23 06:21:40 UTC 2016
        Wed Mar 23 06:21:42 UTC 2016
        Wed Mar 23 06:22:06 UTC 2016
        Wed Mar 23 06:22:08 UTC 2016
        ```

    - Actually I don’t have to stretch my imagination too much to come up with scenarios where this would be useful. It might be nice to freeze the current state of a server while I eat lunch or something.
1. Get process stats with the top command.
    - The docker top command is exactly what it sounds like: top that runs in the container.

        ```console
        $ docker run -d —-name=toptest alpine:3.1 watch "echo 'Testing top'"
        fc54369116fe993ae45620415fb5a6376a3069cdab7c206ac5ce3b57006d4241
        $ docker top toptest
        UID PID … TIME CMD
        root 26339 … 00:00:00 watch "echo 'Testing top'"
        root 26370 … 00:00:00 sleep 2
        ```

    - Some columns removed to make it fit here. There is also a docker stats command that is basically top for all the containers running on a host.
1. View container details with the inspect command.
    - The **inspect** command returns information about a container or an image. Here’s an example of running it on the toptest container from the last example above.

        ```console
        $ docker inspect toptest
        [
          {
            "Id": "fdb3008e70892e14d183f8 ... 020cc34fec9703c821",
            "Created": "2016–03–23T17:45:01.876121835Z",
            "Path": "/bin/sh",
            "Args": [
              "-c",
              "while true; do sleep 2; echo 'Testing top'; done"
            ],
            … and lots, lots more.
          }
        ]
        ```

    - I’ve skipped the bulk of the output because there’s a lot of it. Some of the more valuable bits of intelligence you can get are:
        - Current state of the container. (In the "State" property.)
        - Path to the log history file. (In the "LogPath" field.)
        - Values of set environment vars. (In the "Config.Env" field.)
        - Mapped ports. (In the "NetworkSettings.Ports" field.)
        - Probably the most valuable use of inspect for me in the past has been getting the values of environment vars.
        - Even with largely automated deployments I’ve run into issues in the past where the wrong arg was passed to a command and a container ended up running with vars set to incorrect values. When one of your cloud containers starts choking commands like inspect can be a quick cure.
1. View image layers with the history command.
    - This one is more of a build time diagnostic tool, but the questions it answers sometimes come up in debugging situations as well. The docker history command shows the individual layers that make up an image, along with the commands that created them, their size on disk, and hashes.
    - `$ docker history alpine`
    - The returned table is quite wide so I won’t try to illustrate it here. If you run into a situation where the contents of your image aren’t what you expect, this command may solve your puzzle for you.
1. Run one process in each container.
    - This last one is less of a debugging tip, and more of a best practice that will definitely make debugging, and reasoning about the state of your container a lot easier. Docker containers are meant to run a single process that is PID 1 inside the sandbox. You can make that process a shell and spin up a bunch of stuff in the background, or you can make it supervisord and do the same, but it’s not really what containers are good at and it hobbles systems meant to manage and monitor them.
    - The main benefit of running one process per container is that it’s easier to reason about the state of the container at run time. The container comes up when the process comes up and dies when it dies, and platforms like Docker Compose, kubernetes, and Amazon ECS can see that and restart it. They can also monitor the health (liveness and readiness) of a single-process container, but it is much more difficult to define declaratively what either of those things means when they depend on multiple processes being in good health inside the container.

### Kolla-Ansible Quick Start ( [Catalog](#catalog) )

1. Kolla-Achitecture, reference: [Building a Containerized OpenStack Lab](https://networkop.co.uk/blog/2017/09/08/os-lab-docker/)

    ![](../img/kolla-lab.png)
1. Build an environment with Ansible
    - Topology map

        ![](../src/ansible-build-openstack-env/img/openstack-env-architecture.png)
    - [Ansible Scripts: Build OpenStack Environment](../src/ansible-build-openstack-env)

### Kolla-Ansible Installation & Maintenance ( [Catalog](#catalog) )

1. [OpenStack Stein Kolla Reference](https://docs.openstack.org/kolla-ansible/stein/)
1. [Demo]: [kolla-ansible installation in all-in-one mode](installation-kolla-all-in-one.md)
1. [Demo]: [kolla-ansible installation in multi-node mode](installation-kolla-multinode.md)
1. [Demo]: [kolla-ansible maintenance](maintenance-kolla.md)
    - OpenStack Upgrade
    - OpenStack Nodes Scaling up

## lab-05 OpenStack Debug ( [Catalog](#catalog) )

### Debug with DevStack ( [Catalog](#catalog) )

1. DevStack Installation
    - [Demo]: Devstack Installation
1. DevStack Debugging
    - [Demo]: Debug with DevStack

### Debug with Kolla-Ansible ( [Catalog](#catalog) )

1. Kolla-Ansible Logs
    - [Demo]: Check logs
        - 常用的查看log方法是查看 docker logs container_name 来查看容器的前台进程日志
        - 所有的log存在 `/var/lib/docker/volumes/kolla_logs/_data/{project_name}` 也就是服务进程的后台日志
1. Kolla-Ansible Debugging
    - [Demo]: Kolla-Ansible Debugging
        - 如果是bootstrap容器失败，那么需要检查数据库连接，并且手动登录到数据库，删除对应的库，重新deploy
        - kolla-ansible部署中，加上一个tee或者保存一下日志是个比较好的方法
        - 当容器起不来的时候，可以修改 `/etc/kolla/{service}/` 下面的 `config.json`，把command中的启动命令修改成sleep infinity等命令，那么可以exec到容器里进行代码的调试

### [Optional] RDO ( [Catalog](#catalog) )

1. [Demo]: [RDO Installation](installation-rdo-all-in-one.md)

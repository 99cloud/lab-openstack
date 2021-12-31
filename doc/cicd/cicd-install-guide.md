# CICD 安装指南

## 1. 环境要求

- 多节点部署

    推荐使用 5 台 CentOS 7.9 虚拟机（ISO 镜像可以用 Minimal，安装时选择用 Minimal 安装），分别部署 OIDC、gitlab、gerrit、redmine、drone，每台虚拟机具体配置如下：

    || CPU/核 | 内存/G | 根磁盘/G | 数据盘/G | 数据盘挂载目录 | 网卡/张 |
    | --- | --- | --- | --- | --- | --- | --- |
    | OIDC | 4 | 8 | 100 | 无 | 无 | 1 |
    | gitlab | 4 | 8 | 100 | 无 | 无 | 1 |
    | gerrit | 4 | 8 | 100 | 100 | /external/gerrit | 1 |
    | redmine | 4 | 8 | 100 | 无 | 无 | 1 |
    | drone | 4 | 8 | 100 | 无 | 无 | 1 |

    另外需要安装多个 `drone-docker-runner` 和 `drone-exec-runner` 节点，具体配置如下：

    || CPU/核 | 内存/G | 根磁盘/G | 数据盘/G | 数据盘挂载目录 | 网卡/张 |
    | -------------- | --- | --- | --- | --- | --- | --- |
    | drone-docker-runner | 4 | 8 | 100 | 无 | 无 | 1 |
    | drone-exec-runner | 4 | 8 | 100 | 无 | 无 | 1 |

    推荐使用 3 个节点的 drone docker runner 和 3 节点的 drone exec runner，即:

    - drone-docker-runner-1
    - drone-docker-runner-2
    - drone-docker-runner-3
    - drone-exec-runner-1
    - drone-exec-runner-2
    - drone-exec-runner-3

- AIO（all-in-one）部署

    || CPU/核 | 内存/G | 根磁盘/G | 数据盘/G | 数据盘挂载目录 | 网卡/张 |
    | --- | --- | --- | --- | --- | --- | --- |
    | AIO | 12 | 24 | 150 | 100 | /external/gerrit | 1 |

部署过程中需要从 internet 安装包，因此需要保证虚拟机能够连接 internet。

## 2. 准备工作

各节点安装 docker (官方文档：https://docs.docker.com/engine/install/centos/)

1. 更新依赖仓库

    ```bash
    apt-get update -y || yum update -y
    ```

2. 安装 docker engine

    ```bash
    apt-get install docker.io -y || yum install docker -y
    ```

3. 启用 docker

    ```bash
    systemctl enable docker --now
    ```

4. 安装所需依赖包

    ```console
    yum install gcc libffi-devel make wget -y
    yum group install 'Development Tools' -y
    ```

## 3. 部署

### 3.1 openID

#### 3.1.1 安装 openID 身份服务

1. go 环境准备

    ```bash
    wget https://golang.org/dl/go1.17.3.linux-amd64.tar.gz
    rm -rf /usr/local/go && tar -C /usr/local -xzf go1.17.3.linux-amd64.tar.gz

    export PATH=$PATH:/usr/local/go/bin
    ```

    export 可以写到 ~/.bashrc 中

    ```console
    $ cat ~/.bashrc | grep export
    export GOROOT=/usr/local/go
    export GO111MODULE=on
    export GOPROXY=https://goproxy.cn,direct
    export PATH=$GOROOT/bin:$PATH
    ```

2. 安装 dex (参考文档：https://dexidp.io/docs/getting-started/)

    ```bash
    git clone https://github.com/dexidp/dex.git
    cd dex/
    make build
    ```

3. 更改配置文件 vi dex/examples/config-dev.yaml

    ```yaml
    issuer: http://<openid_ip>:5556/dex

    staticClients:
    - id: example-app
      redirectURIs:
      - 'http://<openid_ip>:5555/callback'
      name: 'Example App'
      secret: ZXhhbXBsZS1hcHAtc2VjcmV0

    # 配置用于登录的用户的静态密码列表
    # 示例：email 为 admin@example.com，密码为 password
    staticPasswords:
    - email: "admin@example.com"
      # bcrypt hash of the string "password": $(echo password | htpasswd -BinC 10 admin | cut -d: -f2)
      hash: "$2a$10$2b2cU8CPhOTaGrs1HRQuAueS7JTT5ZHsHSzYiFPm1leZck7Mc8T4W"
      username: "admin"
      userID: "08a8684b-db88-4b73-90a9-3cd1661f5466"
    ```

4. 启动服务

    ```bash
    cd dex/
    ./bin/dex serve examples/config-dev.yaml

    # 后台运行命令
    # nohup ./bin/dex serve examples/config-dev.yaml &
    ```

5. 可以用 tmux 跑在后台

    ```bash
    yum install tmux -y
    tmux new -s dex

    ./bin/dex serve examples/config-dev.yaml

    # CTRL+b / d

    tmux ls
    # dex: 1 windows (created Sun Nov 14 21:39:32 2021) [158x42]

    # attach
    tmux a -t dex
    ```

#### 3.1.2 [可选] openID 对接 ldap

1. 通过更改 dex 配置文件，对接已有 ldap

    编辑 dex/examples/config-dev.yaml 文件，删除以下配置

    ```yaml
    - type: mockCallback
      id: mock
      name: Example
    ```

    编辑 dex/examples/config-dev.yaml 文件，添加以下配置

    ```yaml
    - type: ldap
      id: ldap
      name: LDAP
      config:
        insecureNoSSL: true
        insecureSkipVerify: true
        startTLS: true
        host: <ldap_ip>
        bindDN: uid=serviceaccount,cn=users,dc=example,dc=com
        bindPW: password

        UserSearch:
          baseDN: cn=users,dc=example,dc=com
          username: sAMAccountName
          emailAttr: mail
          idAttr: sAMAccountName
          nameAttr: givenName
    ```

    例：

    ```yaml
    - type: ldap
      id: ldap
      name: LDAP
      config:
        insecureNoSSL: true
        insecureSkipVerify: true
        startTLS: true
        host: 172.16.30.19:389
        bindDN: cn=gerrit,ou=sys,ou=99cloud,dc=sh,dc=99cloud,dc=net
        bindPW: password

        UserSearch:
          baseDN: ou=99cloud,dc=sh,dc=99cloud,dc=net
          username: sAMAccountName
          emailAttr: mail
          idAttr: sAMAccountName
          nameAttr: givenName
    ```

2. openID 登录流程

- 点击登录按钮后，跳转 dex 登录方式选择界面

    ![](images/dex-1.png)

- 选择 LDAP 登录方式登录，跳转 LDAP 登录界面

    ![](images/dex-2.png)

- 填写 Username 和 Password 后，跳转授权认证页面

    ![](images/dex-3.png)

### 3.2 gitlab

> 官方文档：<https://docs.gitlab.com/ee/install/docker.html#installation>

#### 3.2.1 安装 gitlab

1. 下载 gitlab-ce 社区版镜像

    ```bash
    docker pull gitlab/gitlab-ce:14.4.2-ce.0
    ```

2. 设置卷位置并安装 gitlab，本文中建议的数据卷 mount 路径在 `/srv/gitlab`

    ```bash
    export GITLAB_HOME=/srv/gitlab

    docker run --detach   --hostname gitlab.example.com   --publish 443:443 --publish 80:80  --publish 1122:22  --name gitlab   --restart always   --volume $GITLAB_HOME/config:/etc/gitlab   --volume $GITLAB_HOME/logs:/var/log/gitlab   --volume $GITLAB_HOME/data:/var/opt/gitlab   gitlab/gitlab-ce:14.4.2-ce.0

    # AIO scenaio
    # docker run --detach   --hostname gitlab.example.com   --publish 9001:443 --publish 80:80  --publish 7001:22  --name gitlab   --restart always   --volume $GITLAB_HOME/config:/etc/gitlab   --volume $GITLAB_HOME/logs:/var/log/gitlab   --volume $GITLAB_HOME/data:/var/opt/gitlab   gitlab/gitlab-ce:14.4.2-ce.0
    ```

3. 编辑 /srv/gitlab/config/gitlab.rb 文件，完成后重启 gitlab 容器

    ```conf
    # external_url 'GENERATED_EXTERNAL_URL'
    external_url 'http://<gitlab_ip>'

    gitlab_rails['gitlab_shell_ssh_port'] = 1122
    # AIO scenaio
    # gitlab_rails['gitlab_shell_ssh_port'] = 7001
    ```

4. 检查启动情况

    ```bash
    docker logs gitlab
    # 此时应看到启动过程中没有错误信息

    netstat -putln
    # 此时应能看到 gitlab 开启的端口信息
    ```

5. 验证

    打开 `http://<gitlab_ip>` 网页，如下图成功显示，即为 gitlab 安装成功

    ![](images/gitlab-1.png)

#### 3.2.2 集成 openID

1. 修改配置文件

    vi /srv/gitlab/config/gitlab.rb

    ```ruby
    gitlab_rails['omniauth_enabled'] = true
    gitlab_rails['omniauth_allow_single_sign_on'] = ['openid_connect']
    gitlab_rails['omniauth_sync_email_from_provider'] = 'openid_connect'
    gitlab_rails['omniauth_sync_profile_from_provider'] = ['openid_connect']
    gitlab_rails['omniauth_sync_profile_attributes'] = ['name', 'email']
    gitlab_rails['omniauth_block_auto_created_users'] = false
    gitlab_rails['omniauth_auto_link_ldap_user'] = true
    gitlab_rails['omniauth_auto_link_openid_connect_user'] = true
    gitlab_rails['omniauth_auto_link_user'] = ['openid_connect']
    gitlab_rails['omniauth_providers'] = [
      {
        'name' => 'openid_connect',
        'label' => 'Dex OIDC',
        'args' => {
          'name' => 'openid_connect',
          'scope' => ['openid', 'profile', 'email', "groups", "offline_access"],
          'response_type' => 'code',
          'issuer' => 'http://<openid_ip>:5556/dex',
          'client_auth_method' => 'query',
          'discovery' => true,
          'uid_field' => 'preferred_username',
          'client_options' => {
            'identifier' => 'example-app',
            'secret' => 'ZXhhbXBsZS1hcHAtc2VjcmV0',
            'redirect_uri' => 'http://<gitlab_ip>/users/auth/openid_connect/callback',
            # AIO scenaio
            # 'redirect_uri' => 'http://<gitlab_ip>:80/users/auth/openid_connect/callback',
          }
        }
      }
    ]
    ```

2. 使 gitlab 支持 http 协议的 openID 服务

    > 参考链接：<https://github.com/nov/openid_connect/issues/47>

    在 gitlab 容器中 vi /opt/gitlab/embedded/lib/ruby/gems/2.7.0/gems/openid_connect-1.2.0/lib/openid_connect/discovery/provider/config/resource.rb

    ```diff
    @@ -13,10 +13,17 @@ module OpenIDConnect
                 @host = uri.host
                 @port = uri.port unless [80, 443].include?(uri.port)
                 @path = File.join uri.path, '.well-known/openid-configuration'
    +            @scheme = uri.scheme
                 attr_missing!
               end

               def endpoint
    +            case @scheme
    +            when "http"
    +              SWD.url_builder = URI::HTTP
    +            else
    +              SWD.url_builder = URI::HTTPS
    +            end
                 SWD.url_builder.build [nil, host, port, path, nil, nil]
               rescue URI::Error => e
                 raise SWD::Exception.new(e.message)
    ```

    修改后重启 gitlab 容器

5. 验证

    打开 `http://<gitlab_ip>` 网页，如下图成功显示，并且可以验证 [openID 登录流程](#3.1.2)，即为 openID 对接成功

    ![](images/gitlab-2.png)

问题处理：

- 当登录过程中出现 `Unregistered redirect_uri`

    ```yaml
    # openid 节点 dex/examples/config-dev.yaml 文件中添加 redirectURIs
    redirectURIs:
    - 'http://<gitlab_ip>/users/auth/openid_connect/callback'
    # AIO scenaio
    - 'http://<gitlab_ip>:80/users/auth/openid_connect/callback'
    ```

- 对某个 LDAP 用户进行 gitlab admin 授权

    根据 openID 配置文件中的 staticPasswords 静态密码表中默认设置的 admin 权限用户进行授权

#### 3.2.3 备份 gitlab

1. 备份

    ```bash
    docker exec -t gitlab gitlab-backup create
    ls /srv/gitlab/data/backups/
    ```

2. 出于安全因素考虑，上述命令备份时不会备份 gitlab.rb 和 gitlab-secrets.json 文件，如果有需要，请手动备份

#### 3.2.4 恢复 gitlab 备份

1. 恢复 gitlab.rb 和 gitlab-secrets.json 文件

2. 停止连接到数据库的进程，让 GitLab 的其余部分保持运行(假设备份文件名称为backup_2021_09_28_gitlab_backup.tar)

    ```bash
    docker exec -it gitlab gitlab-ctl stop puma
    docker exec -it gitlab gitlab-ctl stop sidekiq
    docker exec -it gitlab gitlab-ctl status
    ```

3. 恢复备份、重新配置、重启并检查 gitlab

    ```bash
    docker exec -it gitlab gitlab-backup restore BACKUP=backup_2021_09_28
    docker exec -it gitlab gitlab-ctl reconfigure
    docker exec -it gitlab gitlab-ctl restart
    docker exec -it gitlab gitlab-rake gitlab:check SANITIZE=true
    ```

### 3.3 gerrit

> 参考文档：<https://github.com/GerritCodeReview/docker-gerrit>

#### 3.3.1 安装 gerrit

1. 下载镜像

    ```bash
    docker pull gerritcodereview/gerrit:3.3.7-ubuntu20
    ```

2. 启动服务

    ```bash
    # 创建新数据盘 gerrit_volume ，并将该数据盘挂载到 /external 下

    docker run -d --name gerrit -p 80:8080 -p 29418:29418 --volume /external/gerrit/etc:/var/gerrit/etc --volume /external/gerrit/git:/var/gerrit/git --volume /external/gerrit/db:/var/gerrit/db --volume /external/gerrit/index:/var/gerrit/index --volume /external/gerrit/cache:/var/gerrit/cache --env CANONICAL_WEB_URL=http://<gerrit_ip> gerritcodereview/gerrit:3.3.7-ubuntu20

    # AIO scenaio
    # docker run -d --name gerrit -p 8002:8080 -p 29418:29418 --volume /external/gerrit/etc:/var/gerrit/etc --volume /external/gerrit/git:/var/gerrit/git --volume /external/gerrit/db:/var/gerrit/db --volume /external/gerrit/index:/var/gerrit/index --volume /external/gerrit/cache:/var/gerrit/cache --env CANONICAL_WEB_URL=http://<gerrit_ip>:8002 gerritcodereview/gerrit:3.3.7-ubuntu20
    ```

    注：若提示无权限操作，则对/external/gerrit下的路径提权（`chmod -R 777 /external/gerrit/*`），再重新运行的 `docker run` 命令

#### 3.3.2 集成 openID

1. 修改认证配置，并允许远程安装插件

    `vi /external/gerrit/etc/gerrit.config`

    ```
    [auth]
            type = DEVELOPMENT_BECOME_ANY_ACCOUNT
    [plugins]
            allowRemoteAdmin = true
    ```

2. 重启容器：`docker restart gerrit`

3. gerrit 配置

> **注:** AIO scenaio 模式下，网页为 `http://<gerrit_ip>:8002`

- 打开 `http://<gerrit_ip>` 网页，如图显示页面

    ![](images/gerrit-1.png)

- 点击 `New Account` 按钮，刷新 `http://<gerrit_ip>` 网页，如图显示页面

    ![](images/gerrit-2.png)

- 点击 `1000000` 按钮，使用 ID 为 1000000 的用户直接登录，设置 username 为 admin，并上传 gerrit 节点的 SSH key

    > **注:** 若是使用 email 对接，username 值不能与静态密码表中的值相同，即静态密码表中若有用户名为 admin 的用户，则此处 ID 为 1000000 的用户 username 不能为 admin

    ![](images/gerrit-3.png)

4. 安装插件

    ```bash
    ssh -p 29418  <admin_username>@<gerrit_ip> gerrit plugin ls -a

    # 安装 oauth 插件
    ssh -p 29418  <admin_username>@<gerrit_ip> gerrit plugin add https://gerrit-ci.gerritforge.com/job/plugin-oauth-bazel-master-stable-3.4/lastSuccessfulBuild/artifact/bazel-bin/plugins/oauth/oauth.jar

    # 安装 admin-console 插件并查看 users
    ssh -p 29418  <admin_username>@<gerrit_ip> gerrit plugin add https://gerrit-ci.gerritforge.com/job/plugin-admin-console-bazel-master-stable-3.4/lastSuccessfulBuild/artifact/bazel-bin/plugins/admin-console/admin-console.jar
    ssh -p 29418  <admin_username>@<gerrit_ip> admin-console ls-users

    # 查看 groups 并将用户加入到指定组下，即把 ID 为 1000000 的用户加入到 Administrators 组下，赋予管理员权限
    ssh -p 29418  <admin_username>@<gerrit_ip> gerrit ls-groups
    ssh -p 29418  <admin_username>@<gerrit_ip> gerrit set-members --add 1000000 Administrators
    ```

5. 再次修改配置

    vi /external/gerrit/etc/gerrit.config

    ```
    [auth]
            type = OAUTH
    [plugins]
            allowRemoteAdmin = true
    [plugin "gerrit-oauth-provider-dex-oauth"]
            domain = example.com  # 邮箱后缀名，如："99cloud.net"
            root-url = "http://<openid_ip>:5556"
            client-id = "example-app"
            client-secret = "ZXhhbXBsZS1hcHAtc2VjcmV0"
    ```

    重启容器：`docker restart gerrit`

6. 验证

    > **注:** AIO scenaio 模式下，网页为 `http://<gerrit_ip>:8002`

    打开 `http://<gerrit_ip>` 网页，如下图成功显示，并且可以验证 [openID 登录流程](#3.1.2)，即为 openID 对接成功

    ![](images/gerrit-4.png)

问题处理：

- 当登录过程中出现 `Unregistered redirect_uri`

    ```bash
    # openid 节点 dex/examples/config-dev.yaml 文件中添加 redirectURIs
    redirectURIs:
    - 'http://<gerrit_ip>/oauth'
    # AIO scenaio
    # - 'http://<gerrit_ip>:8002/oauth'
    ```

- 对某个 LDAP 用户进行 gerrit admin 授权

    ```bash
    ssh -p 29418 <admin_username>@<gerrit_ip> admin-console ls-users
    ssh -p 29418 <admin_username>@<gerrit_ip> gerrit ls-groups
    ssh -p 29418 <admin_username>@<gerrit_ip> gerrit set-members --add <user_id> Administrators
    ```

#### 3.3.3 备份 gerrit

由于 gerrit 所有主要数据都存储在 git 中，所以通过对文件系统创建快照的方式制作备份即可，即对数据盘 gerrit_volume 硬盘做快照 gerrit_snapshot

#### 3.3.4 恢复 gerrit 备份

从快照 gerrit_snapshot 创建新的云硬盘 gerrit_volume_new，并挂载到机器上即可完成对 gerrit 备份的恢复

### 3.4 redmine

> 参考文档：<https://github.com/sameersbn/docker-redmine#installation>
> 参考文档：<https://www.cnblogs.com/qianxunman/p/12787219.html>

#### 3.4.1 安装 redmine

1. 下载最新版本 redmine

    ```bash
    docker pull redmine:4.2.3
    ```

2. 启动内置 PostgreSQL 和 redmine 容器

    > 更多可用的配置参数可参考：<https://github.com/sameersbn/docker-redmine#available-configuration-parameters>

    ```bash
    docker run -d --name redmine-postgresql -e POSTGRES_PASSWORD=password -e POSTGRES_USER=redmine --volume=/srv/docker/redmine/postgresql:/var/lib/postgresql postgres:9.6.24

    docker run -d --name redmine -e REDMINE_DB_USERNAME=redmine -e REDMINE_DB_PASSWORD=password -p 3000:3000 -v /srv/docker/redmine/redmine/plugins:/usr/src/redmine/plugins -v /srv/docker/redmine/redmine/files:/usr/src/redmine/files --link redmine-postgresql:postgres redmine:4.2.3
    # AIO scenaio
    docker run -d --name redmine -e REDMINE_DB_USERNAME=redmine -e REDMINE_DB_PASSWORD=password -p 3001:3000 -v /srv/docker/redmine/redmine/plugins:/usr/src/redmine/plugins -v /srv/docker/redmine/redmine/files:/usr/src/redmine/files --link redmine-postgresql:postgres redmine:4.2.3
    ```

    重启 redmine 容器：`docker restart redmine`

3. 验证

    > **注:** AIO scenaio 模式下，网页为 `http://<redmine_ip>:3001`

    打开 `http://<redmine_ip>:3000` 网页

    ![](images/redmine-1.png)

    登录 redmine，并修改 admin 密码

    ![](images/redmine-2.png)
    - username: `admin`
    - password: `admin`

#### 3.4.2 集成 openID

1. 安装插件并重新启动容器

    ```bash
    cd /srv/docker/redmine/redmine/plugins
    git clone https://github.com/devopskube/redmine_openid_connect.git
    ```

    注：该插件目前有 bug 需手动修复
    - /srv/docker/redmine/redmine/plugins/redmine_openid_connect/lib/redmine_openid_connect/account_controller_patch.rb:105

        ```ruby
        user.login = user_info["user_name"] || user_info["nickname"] || user_info["preferred_username"] || user_info["email"]

          firstname: firstname || "firstname",
          lastname: lastname || "lastname",
        ```
    - /srv/docker/redmine/redmine/plugins/redmine_openid_connect/app/models/oic_session.rb:99

        ```ruby
        def self.parse_token(token)
           jwt = token.split('.')
           begin
             return JSON::parse(Base64::decode64(jwt[1]))
           rescue => exception
             return JSON::parse(Base64::urlsafe_decode64(jwt[1]))
           end
         end
        ```

    在 docker 容器中，运行 bundle 命令，完成后重启容器

    ```bash
    bundle install
    bundle exec rake redmine:plugins:migrate RAILS_ENV=production
    ```

2. 界面配置插件

    在 `设置 -> 管理 -> 插件` 中，选择 `Redmine Openid Connect plugin` 插件，配置并保存

    ![](images/redmine-plugin.png)
    - Client ID: `example-app`
    - OpenID Connect server url: `http://<openid_ip>:5556/dex`
    - Client Secret: `ZXhhbXBsZS1hcHAtc2VjcmV0`
    - OpenID Connect scopes: `profile,openid,email,groups,offline_access`

3. 验证

    > **注:** AIO scenaio 模式下，网页为 `http://<redmine_ip>:3001`

    打开 `http://<redmine_ip>:3000` 网页，如下图成功显示，并且可以验证 [openID 登录流程](#3.1.2)，即为 openID 对接成功

    ![](images/redmine-3.png)

问题处理：

- 当登录过程中出现 `Unregistered redirect_uri`

    ```yaml
    # openid 节点 dex/examples/config-dev.yaml 文件中添加 redirectURIs
    redirectURIs:
    - 'http://<redmine_ip>:3000/oic/local_login'
    # AIO scenaio
    # - 'http://<redmine_ip>:3001/oic/local_login'

    # redmine 容器中 /usr/src/redmine/config/settings.yml 文件中修改 host_name
    host_name:
      default: <redmine_ip>:3000
    # AIO scenaio
    #  default: <redmine_ip>:3001
    ```

#### 3.4.3 备份 redmine

```bash
docker commit -p <redmine_container_id> redmine-backup-xxxxxxxx
docker save -o ~/redmine-backup-xxxxxxxx.tar redmine-backup-xxxxxxxx
```

#### 3.4.4 恢复备份

```bash
# 恢复备份之前，停止并删除正在运行的容器
docker stop redmine && docker rm redmine

docker load -i ~/redmine-backup-xxxxxxxx.tar
docker run -d --name redmine -e REDMINE_DB_USERNAME=redmine -e REDMINE_DB_PASSWORD=password -p 3000:3000 -v /srv/docker/redmine/redmine/plugins:/usr/src/redmine/plugins -v /srv/docker/redmine/redmine/files:/usr/src/redmine/files --link redmine-postgresql:postgres redmine-backup-xxxxxxxx
# AIO scenaio
docker run -d --name redmine -e REDMINE_DB_USERNAME=redmine -e REDMINE_DB_PASSWORD=password -p 3001:3000 -v /srv/docker/redmine/redmine/plugins:/usr/src/redmine/plugins -v /srv/docker/redmine/redmine/files:/usr/src/redmine/files --link redmine-postgresql:postgres redmine-backup-xxxxxxxx
```

### 3.5 drone

#### 3.5.1 drone server 安装

1. gitlab 配置

- 在 `User Settings -> Applications` 中添加 New application，并获得 `Application ID` 和 `Secret`

    ![](images/drone-gitlab-1.jpg)

    > **注:** 在 AIO scenaio 的情况下，设置 `http://<drone_ip>:8003/login`

    ![](images/drone-gitlab-2.jpg)

- 在 `Admin Area -> Network` 中设置 Outbound requests

    ![](images/drone-gitlab-3.jpg)

2. 拉取 drone 镜像并启动服务

    > **注：**

    ```bash
    # $GITLAB_CLIENT_ID 为步骤 1 中获取的 Application ID
    # $GITLAB_CLIENT_SECRET 为步骤1中获取的 Secret
    DRONE_RPC_SECRET=$(openssl rand -hex 16)
    ADMIN_USER_TOKEN=$(openssl rand -hex 16)
    ```

    ```bash
    docker pull drone/drone:2.4.0

    docker run \
    --volume=/srv/docker/drone:/var/lib \
    --env=DRONE_GITLAB_SERVER=http://<gitlab_ip> \
    --env=DRONE_GITLAB_CLIENT_ID=$GITLAB_CLIENT_ID \
    --env=DRONE_GITLAB_CLIENT_SECRET=$GITLAB_CLIENT_SECRET \
    --env=DRONE_RPC_SECRET=$DRONE_RPC_SECRET \
    --env=DRONE_SERVER_HOST=<drone_server_ip> \
    --env=DRONE_SERVER_PROTO=http \
    --env=DRONE_USER_CREATE=username:<drone_admin_username>,admin:true,token:$ADMIN_USER_TOKEN \
    --publish=80:80 --publish=443:443 \
    --restart=always \
    --detach=true \
    --name=drone drone/drone:2.4.0

    # AIO scenaio
    # docker run \
    # --volume=/srv/docker/drone:/var/lib \
    # --env=DRONE_GITLAB_SERVER=http://<gitlab_ip>:80 \
    # --env=DRONE_GITLAB_CLIENT_ID=$GITLAB_CLIENT_ID \
    # --env=DRONE_GITLAB_CLIENT_SECRET=$GITLAB_CLIENT_SECRET \
    # --env=DRONE_RPC_SECRET=$DRONE_RPC_SECRET \
    # --env=DRONE_SERVER_HOST=<drone_server_ip>:8003 \
    # --env=DRONE_SERVER_PROTO=http \
    # --env=DRONE_USER_CREATE=username:<drone_admin_username>,admin:true,token:$ADMIN_USER_TOKEN \
    # --publish=8003:80 --publish=9003:443 \
    # --restart=always \
    # --detach=true \
    # --name=drone drone/drone:2.4.0
    ```

3. 验证

> **注:** 在 AIO scenaio 的情况下，网页为 `http://<drone_ip>:8003`

- 登录 gitlab，打开 `http://<drone_server_ip>` 网页，跳转 drone 验证页面

    ![](images/drone-1.png)

- 点击 `continue` 按钮，跳转授权页，自动重定向到 drone 注册页面，完成注册即可登录

    ![](images/drone-2.png)

    > **注**：drone 注册页面 Name 值若填写为 docker run 启动服务 中的 `<drone_admin_username>` 值，即为 admin 用户注册

4. drone CLI 安装与配置

    ```bash
    # 安装
    curl -L https://github.com/drone/drone-cli/releases/v1.4.0/download/drone_linux_amd64.tar.gz | tar zx
    sudo install -t /usr/local/bin drone

    # 配置
    export DRONE_SERVER=http://<drone_server_ip>:8003
    export DRONE_TOKEN=$ADMIN_USER_TOKEN

    # 验证
    drone info
    ```

问题处理：

- 对 drone 某个非 admin 用户进行 admin 授权

    ```
    # CLI
    export DRONE_SERVER=http://<drone_server_ip>:8003
    export DRONE_TOKEN=$ADMIN_USER_TOKEN
    drone user update <username> --admin
    ```

#### 3.5.2 drone docker runner 安装

1. 拉取 drone 镜像并启动 drone runner docker 服务

    > **注：** $DRONE_RPC_SECRET 与 drone server 中设置的一致

    ```bash
    docker pull drone/drone-runner-docker:1.7.0

    docker run -d -v /var/run/docker.sock:/var/run/docker.sock \
    -e DRONE_RPC_PROTO=http \
    -e DRONE_RPC_HOST=<drone_server_ip> \
    -e DRONE_RPC_SECRET=$DRONE_RPC_SECRET \
    -e DRONE_RUNNER_CAPACITY=2 \
    -e DRONE_RUNNER_NAME=<drone_runner_name> \
    -p 80:80 --restart always --name runner \
    drone/drone-runner-docker:1.7.0

    # AIO scenaio
    # docker run -d -v /var/run/docker.sock:/var/run/docker.sock \
    # -e DRONE_RPC_PROTO=http \
    # -e DRONE_RPC_HOST=<drone_server_ip>:8003 \
    # -e DRONE_RPC_SECRET=$DRONE_RPC_SECRET \
    # -e DRONE_RUNNER_CAPACITY=2 \
    # -e DRONE_RUNNER_NAME=<drone_runner_name> \
    # -p 8004:80 --restart always --name runner \
    # drone/drone-runner-docker:1.7.0
    ```

2. 验证

- gitlab 上创建 Group，名称为 `99cloud`；创建项目，名称为 `skyline`

- 登录 drone，同步 gitlab 项目，进入 `skyline -> Settings` 中，点击 activate 按钮激活并配置

    ![](images/drone-3.png)

- 本地拉取 skyline 项目，添加 skyline/.drone.yml 文件，执行 `git push`，查看 drone 界面，显示 EXECUTIONS 已完成

    ```yaml
    # .drone.yml 示例文档
    kind: pipeline
    type: docker
    name: tools-drone

    steps:
      - name: test
        image: alpine
        commands:
          - echo hello
    trigger:
      event:
        - push
    ```

#### 3.5.3 drone exec runner 安装

1. 下载并安装 drone runner exec

    ```bash
    curl -L https://github.com/drone-runners/drone-runner-exec/releases/download/v1.0.0-beta.9/drone_runner_exec_linux_amd64.tar.gz | tar zx
    sudo install -t /usr/local/bin drone-runner-exec
    ```

2. 配置并启动 drone runner exec 服务

    > **注：** $DRONE_RPC_SECRET 与 drone server 中设置的一致

    ```bash
    mkdir -p /etc/drone-runner-exec
    mkdir -p /var/log/drone-runner-exec

    echo "DRONE_RPC_PROTO=http" >> /etc/drone-runner-exec/config
    echo "DRONE_RPC_HOST=<drone_server_ip>" >> /etc/drone-runner-exec/config
    # AIO scenaio
    # echo "DRONE_RPC_HOST=<drone_server_ip>:8003" >> /etc/drone-runner-exec/config
    echo "DRONE_RPC_SECRET=$DRONE_RPC_SECRET" >> /etc/drone-runner-exec/config
    echo "DRONE_RUNNER_CAPACITY=4" >> /etc/drone-runner-exec/config
    echo "DRONE_RUNNER_NAME=<drone_exec_name>" >> /etc/drone-runner-exec/config
    echo "DRONE_DEBUG=true" >> /etc/drone-runner-exec/config
    echo "DRONE_LOG_FILE=/var/log/drone-runner-exec/log.txt" >> /etc/drone-runner-exec/config

    drone-runner-exec service install
    drone-runner-exec service start
    ```

3. 验证

    ```bash
    cat /var/log/drone-runner-exec/log.txt

    # log 正常输出
    # starting the server
    # successfully pinged the remote server
    ```

### 3.6 gerrit 同步 gitlab

#### 3.6.1 项目初始化

> **注**: 确保 gerrit 和 gitlab 上有相同名称的项目，例如 99cloud/skyline

1. gerrit 上分别创建 Repository : `99cloud` 和 `99cloud/skyline` ，且 `99cloud/skyline` 权限继承自 `99cloud`

2. gitlab 上创建 Group，名称为 `99cloud`；创建项目，名称为 `skyline`

3. 将 gerrit 节点公钥传至 gitlab 的 SSH Keys，并手动同步 gerrit 下的 git 仓库

    > skyline.git 文件权限需要与 gerrit 其他仓库文件权限一致

    ```bash
    cd /external/gerrit/git/99cloud
    rm -rf skyline.git
    git clone --bare ssh://git@<gitlab_ip>:1122/99cloud/skyline.git
    ```

#### 3.6.2 认证相关配置

1. gerrit 容器内生成密钥对

    ```bash
    docker exec -it -ugerrit gerrit bash

    # 密钥对默认位置为 /var/gerrit/.ssh/id_rsa 及 /var/gerrit/.ssh/id_rsa.pub
    ssh-keygen -m PEM -t rsa
    ```

2. 将生成的公钥传至 gitlab 的 SSH Keys

    ![](images/ssh-key.jpg)

3. gerrit 容器内配置 ~/.ssh/config 文件，配置完成后重启容器

    ```text
    Host <gitlab_ip>
        Port 1122
        # AIO scenaio
        # Port 7001
        IdentityFile /var/gerrit/.ssh/id_rsa # 私钥路径
        UserKnownHostsFile /dev/null
        StrictHostKeyChecking no
    ```

#### 3.6.3 插件配置

编辑 `/external/gerrit/etc/replication.config`，进行 gerrit replication 插件配置

```ini
[gerrit]
    autoReload = true
    replicateOnStartup = false
[replication]
    lockErrorMaxRetries = 5
    maxRetries = 5
[remote "gitlab"]
    url = ssh://git@<gitlab_ip>:1122/${name}.git
    # AIO scenaio
    # url = ssh://git@<gitlab_ip>:7001/${name}.git
    push = +refs/heads/*:refs/heads/*
    push = +refs/tags/*:refs/tags/*
    threads = 3
    projects = "^.*/.*"
```

#### 3.6.4 验证

```bash
# 插件 reload
ssh -p 29418 <admin_username>@<gerrit_ip> gerrit plugin reload replication

ssh -p 29418 <admin_username>@<gerrit_ip> replication list
# Remote: gitlab
# Url: ssh://git@<gitlab_ip>:1122/${name}.git
# AIO scenaio
# Url: ssh://git@<gitlab_ip>:7001/${name}.git

# 开始同步命令
ssh -p 29418 <admin_username>@<gerrit_ip> replication start 99cloud/skyline

# 容器内可查看日志
vi /var/gerrit/logs/replication_log
# Replication to ssh://git@<gitlab_ip>:1122/99cloud/skyline.git completed
# AIO scenaio
# Replication to ssh://git@<gitlab_ip>:7001/99cloud/skyline.git completed
```

### 3.7 gerrit webhooks 与 drone

#### 3.7.1 gerrit webhooks 配置

编辑 `/external/gerrit/etc/gerrit.config` 文件，进行 webhooks 全局配置

```ini
[plugin "webhooks"]
    connectionTimeout = 3000
    socketTimeout = 2500
    maxTries = 3
    retryInterval = 2000
    threadPoolSize = 3
```

```bash
git clone "ssh://<admin_username>@<gerrit_ip>:29418/All-Projects"
cd All-Projects/
git fetch origin refs/meta/config:refs/remotes/origin/meta/config && git checkout meta/config
```

在 All-Projects/ 目录下创建并编辑 `webhooks.config` 文件

```ini
[remote "patchsetcreated"]
  url = http://<testserver_ip>:8899
  event = patchset-created
```

```bash
git add webhooks.config
git commit -am "Add webhooks config file"
git push origin meta/config:meta/config
```

#### 3.7.2 drone配置

> **注**：
> git version 需 2.2 以上且已安装 git-review
> gerrit 上有 Repository : `99cloud` 和 `99cloud/skyline` ，且 `99cloud/skyline` 权限继承自 `99cloud`
> gitlab 上有 Group，名称为 `99cloud`；创建项目，名称为 `skyline`
> gerrit 自动同步 gitlab

本地拉取 gerrit skyline 项目

```bash
cd skyline/
# 添加 commit-msg hooks
gitdir=$(git rev-parse --git-dir); scp -p -P 29418 <username>@<gerrit_ip>:hooks/commit-msg ${gitdir}/hooks/
```

skyline 项目中添加文件 `.gitreview`

```ini
# .gitreview文件
[gerrit]
host=<gerrit_ip>
port=29418
project=<project_name>
defaultbranch=<default_branch_name>
```

skyline 项目中编辑 `.drone.yml`

```yaml
# .drone.yml 示例文件
# 更多请参考 https://docs.drone.io/
kind: pipeline
type: docker
name: drone-custom-review

steps:
  - name: test
    image: centos:7
    depends_on: [clone]
    commands:
      - yum install git -y
      - mkdir -p ~/.ssh
      - echo -e $SSHKEY >> ~/.ssh/id_rsa
      - cat ~/.ssh/id_rsa
      - chmod 600 ~/.ssh/id_rsa
      - mkdir -p /etc/ssh
      - echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
      - git fetch ssh://$USER_NAME@$GERRIT_IP:$GERRIT_PORT/${PROJECT_NAME} ${REF} && git cherry-pick FETCH_HEAD
      - echo test
      - ssh -p $GERRIT_PORT $USER_NAME@$GERRIT_IP gerrit review ${COMMIT} --code-review +1
    environment:
      USER_NAME:
        from_secret: username
      GERRIT_IP:
        from_secret: gerritip
      GERRIT_PORT:
        from_secret: gerritport
      SSHKEY:
        from_secret: sshkey

trigger:
  event:
    - custom
```

```bash
git add .
git commit -am "Add review config file"
git push
```

> **注**:
> `<drone_admin_user>`: gerrit review 用户可直接使用 admin 权限用户，或者另外设置 drone review 权限用户
> 如，`cat <is_rsa.pub> | ssh -p 29418 <admin_username>@<gerrit_ip> gerrit create-account --ssh-key - <drone_admin_user>` 创建 drone review 用户
> `<id_rsa>`: 该私钥需要进行格式化处理
> 如，格式化处理为：`-----BEGIN RSA PRIVATE KEY-----\nxxx\n-----END RSA PRIVATE KEY-----`

登录 drone admin 账号，在 `drone->99cloud/skyline->settings->secrets` 界面配置 `Secrets`

- `username`:`<drone_admin_user>` # gerrit review 用户名
- `gerritip`:`<gerrit_ip>`
- `gerritport`:`<gerrit_port>`
- `sshkey`:`<id_rsa>` # gerrit review 用户私钥

在 gerrit 的 review 用户中配置 `<id_rsa>` 对应公钥 `<is_rsa.pub>`

#### 3.7.3 验证

```bash
yum install python3 -y
pip3 install request
```

新建并编辑 `test_webhooks.py` 文件

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests

host = ('0.0.0.0', 8899)

class Resquest(BaseHTTPRequestHandler):
    def do_POST(self):
        req_datas = self.rfile.read(int(self.headers['content-length']))
        parsed = json.loads(req_datas.decode())
        print(parsed)
        data = {'result_code': 'Success'}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        branch = parsed["change"]["branch"]
        project = parsed["change"]["project"]
        ref = parsed["patchSet"]["ref"]
        commit = parsed["patchSet"]["revision"]
        url = 'http://<drone_ip>/api/repos/'+ project +'/builds'
        # AIO scenaio
        # url = 'http://<drone_ip>:8003/api/repos/'+ project +'/builds'
        headers = {'Authorization':'<drone admin authorization>'}
        # <drone admin authorization> 值可查看 drone界面 -> Account Settings -> Example API Usage
        params = {'branch': branch, 'PROJECT_NAME': project, 'REF': ref, 'COMMIT': commit}
        res = requests.post(url, params=params, headers=headers)
        print(res)

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
```

启动测试环境，测试环境 ip 为 `<testserver_ip>`

```bash
python3 test_webhooks.py
```

- 测试
    - 对 99cloud/skyline 进行 `git review` 操作
    - 查看 test server 服务器可见 response 200
    - 查看 `drone -> 99cloud/skyline -> Builds` 界面可见 EXECUTIONS

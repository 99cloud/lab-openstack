# 使用社区代码制作 kolla 包

## 官方文档

> **注：** 此处为 openstack 最新版官方文档，其他版本文档请在目录中选择更换，参考：<https://releases.openstack.org/wallaby/index.html>

[kolla build 官方文档](https://docs.openstack.org/kolla/latest/admin/image-building.html)

## 机器要求

- centos 7.9 / 8 / ubuntu 20.04 都可以，以 7.9 为例：
- 安装 kolla：

    ```bash
    yum install python3
    # wallaby 是 12.0.1
    python3 -m pip install kolla==12.0.1
    ```

- 安装 git：`yum install -y git`
- 安装并启用 docker

    ```bash
    yum install -y docker
    systemctl enable docker --now
    ```

## 环境准备

```console
# kolla-build --version
12.0.1
```

## 启动 docker registry

```console
docker run -d -p 4000:5000 --restart=always -v /opt/registry/:/var/lib/registry --name registry registry:2
```

## docker 设置

vim /etc/docker/daemon.json 文件

```json
{ "insecure-registries":["<docker_registry_ip>:4000"] }
```

设置后重启 docker

```bash
systemctl restart docker
```

## 设置配置文件

vi kolla-build.conf

```bash
[DEFAULT]
debug = true
base = centos
install_type = source
namespace = kolla
registry = <docker_registry_ip>:4000
tag = master
retries = 5
push = true
push_threads = 1
log_dir = /root/kolla/log

tarballs_base = <tarballs_base_ip>

[profiles]
openstack = cinder, glance, heat, horizon, ironic, neutron, nova, octavia, placement, keystone
```

- registry：registry 仓库地址
- install_type：，构建镜像方式，可选择 `binary/source`
- tag：镜像 tag
- push：build images 之后是否向 registry 推送镜像
- tarballs_base：源码包地址，默认为`http://tarballs.opendev.org/`
- openstack：需要 build 的组件列表

当 install_type 为 source 时，kolla-build.conf 可以自定义镜像的 source 源

- url：location 为 tarball 地址
- git：location 为 git 地址
- local：location 为本地 tarball 地址或者本地源码地址

```
# kolla-build.conf
[glance-base]
type = url
location = https://tarballs.openstack.org/glance/glance-master.tar.gz

[keystone-base]
type = git
location = https://opendev.org/openstack/keystone
reference = stable/mitaka

[heat-base]
type = local
location = /home/kolla/src/heat

[ironic-base]
type = local
location = /tmp/ironic.tar.gz
```

## build 镜像

```console
kolla-build --profile openstack --config-file kolla-build.conf
```

## 手动打包

```console
# registry.tar.gz
cd /opt/registry/
tar -czvf /root/registry.tar.gz docker/

# 为防止 registry.tar.gz 移动过程中出错，可以记录校验值
sha256sum registry.tar.gz
```

## 部署环境中更新 kolla 包

> **注：** registry 挂载路径建议配置一致，如 `/opt/registry/` ，如果路径不一致可能导致 registry 无法找到正确的数据目录

```console
# tar -xzvf /root/registry.tar.gz -C /opt/registry/

# 启动 registry
docker run -d -p 4000:5000 --restart=always -v /opt/registry/:/var/lib/registry --name registry registry:2

# 验证
curl -X GET <docker_registry_ip>:4000/v2/_catalog
```



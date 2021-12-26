# 使用社区代码制作 kolla 包

参考 Kolla 官方文档：<https://docs.openstack.org/kolla/latest/admin/image-building.html>

## 机器要求

- centos 8（CentOS 7.9 或者 Ubuntu 20.04 也行）
- 安装 kolla
- 安装 git
- 安装并启用 docker

## 启动 docker registry

```console
$ docker run -d -p 4000:5000 --restart=always -v /opt/registry/:/var/lib/registry --name registry registry:2
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
- tag：镜像 tag
- tarballs_base：源码包地址，默认为`http://tarballs.opendev.org/`
- openstack：需要 build 的组件列表

可以从源码 build 镜像

```ini
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
$ kolla-build --profile openstack --config-file kolla-build.conf
```

## 手动打包

```console
$ tar -cvf registry.tar /opt/registry/
```

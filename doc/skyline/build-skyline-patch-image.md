# 构建带 `patch` 的社区 `skyline` 镜像

当某个功能不进入社区，但是需要将该功能打包入镜像中，则进行下面的操作。

## 切换到对应的 `commit id`

根据 patch 所对应的 `commit id`，选择更新或后退到指定 `commit id`，`commit id` 与 `patch` 的对应关系如下

| commit_id                                | patch                                                                            |
| ---------------------------------------- | -------------------------------------------------------------------------------- |
| 0aaca80308082b9f736e2c466a65efc28f0ab7b8 | [skyline patch](skyline-patch/0001-Animbus-feature-add-instance-top5-monitor.patch) |

## 修改 `Makefile` 文件

把 `patch` 文件移动到项目根目录下，添加到 `build` 命令下面

```Makefile
.PHONY: build
BUILD_ENGINE ?= docker
BUILD_CONTEXT ?= .
DOCKER_FILE ?= container/Dockerfile
IMAGE ?= skyline
IMAGE_TAG ?= latest
ifeq ($(BUILD_ENGINE), docker)
    build_cmd = docker build
else ifeq ($(BUILD_ENGINE), buildah)
    build_cmd = buildah bud
else
    $(error Unsupported build engine $(BUILD_ENGINE))
endif
build:
	if [ ! -e "libs/skyline-console/.git" ]; then git submodule update --init; fi
	cp <patch_file_name> ./libs/skyline-console
	cd ./libs/skyline-console \
	&& git apply --check <patch_file_name> \
	&& git apply <patch_file_name> 
	$(build_cmd) --no-cache --pull --force-rm --build-arg RELEASE_VERSION=$(RELEASE_VERSION) --build-arg GIT_BRANCH=$(GIT_BRANCH) --build-arg GIT_COMMIT=$(GIT_COMMIT) $(BUILD_ARGS) -f $(DOCKER_FILE) -t $(IMAGE):$(IMAGE_TAG) $(BUILD_CONTEXT)
```

## 打包镜像

使用命令 `make build` 执行镜像打包

# 通过浏览器工具查页面逻辑对应的 API

本文将以创建云主机为例，介绍如何使用 `Chrome` 开发者工具获取前端调用的所有 `API` 请求。

## 1. 进入云主机页面

然后打开 `Chrome` 的开发者工具，[打开方式](troubleshooting_guide.html#问题排查)

将 `Network` 和 `Console` 清空

![清空控制台](./images/163160901267.png)

![image-20210914164550583](./images/image-20210914164550583.png)

## 2. 进入云主机创建界面

保持 `Network` 处于打开状态，点击`创建云主机`。此时可以观察到 `Network`中出现了大量的请求。我们点击 `Fetch/XHR` 进行筛选，只留下 `API` 请求。

![image-20210914164935327](./images/image-20210914164935327.png)

其中，各个请求的目标，参见[云主机创建](front-api/instance/create.html)

## 3. 查看请求的详细信息

左键单击目标请求，即可查看到请求的详细信息。

在 `Headers` 中，我们可以看到请求的`General`，`Response Headers`，`Request Headers`，`Parameters`等信息，展开即可查看对应的信息。

比如 `General` 中就展示了请求的基础信息

![image-20210914165818682](./images/image-20210914165818682.png)

`Request Headers` 中展示了请求头的信息

![image-20210914170326659](./images/image-20210914170326659.png)

`Query String Parameters` 中展示了 `Query` 参数

![image-20210914170606772](./images/image-20210914170606772.png)

> 注意： Path 参数不会在这里显示。 需要仔细手动翻找，也可以通过 `Filter` 框过滤。 如下：
> ![image-20210914170902739](./images/image-20210914170902739.png)

## 4. 查看响应

左键单击目标请求，切换 `Tab` 到 `Response`，即可查看响应的内容，响应头可以在 `Headers` 中查看 `Response Headers`。

![image-20210914165833555](./images/image-20210914165833555.png)

![image-20210914165852559](./images/image-20210914165852559.png)

如果响应是 `JSON` 格式，还可以点击 `Preview` 查看格式化后的信息。

![image-20210914165906652](./images/image-20210914165906652.png)

## 复制请求

复制目标请求，可以通过右击该请求，选择 `Copy as fetch` 或者 `Copy as cURL`

![image-20210914171430358](./images/image-20210914171430358.png)

如果是 `fetch`，可以打开 `Console`，将请求粘贴到控制台，回车，即可再次在浏览器端发送请求。

`cURL (bash)` 是在 `Linux` 环境下执行的，由执行的 `Linux` 机器发送请求。

> Bash 是 Linux 环境下的\
> CMD 是 windows 环境下的

## 最终创建云主机的 POST 请求

最终，创建云主机的 `POST` 请求如下：

![image-20210914172332327](./images/image-20210914172332327.png)

`Request Payload` 中可以清晰的看到请求体的内容

其 `fetch` 请求如下：

```js
fetch("https://172.20.154.250/api/openstack/regionone/nova/v2.1/servers", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "openstack-api-version": "compute 2.79",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-auth-token": "gAAAAABhQGCSgtdk-iC16-oeqB6s-99OkZ7MfZW7fyfmqwEYYn6SbHGZJxeCiBYZPYA8dEKZ1yXPLme-ytN6m3uGQFQY3LA3xp6gBIgfcIeehmn0BQH031Y3C3KPndEF1BdyV3McK3ZuJN8EpC4B0hFqFVmTWXhsCsdq_ajetDjZGEq1vB8CvXGcYNaRB0bevf6XQxHXC5BP",
    "x-openstack-request-id": "req-eea89465-189f-4c06-8a42-065233c6d931"
  },
  "referrer": "https://172.20.154.250/compute/instance/create",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "{\"server\":{\"security_groups\":[{\"name\":\"22e8def6-29cd-4bf5-ba8b-7339440dddde\"}],\"name\":\"demacia\",\"flavorRef\":\"19cf6f69-ccb3-4c83-85f9-f2490b18fc48\",\"availability_zone\":\"nova\",\"block_device_mapping_v2\":[{\"boot_index\":0,\"uuid\":\"2153561a-d5ee-4ad0-8df3-f45932830e8d\",\"source_type\":\"image\",\"destination_type\":\"volume\",\"volume_size\":10,\"volume_type\":\"6bb064b6-a240-48d2-ac75-d1bc9257d888\",\"delete_on_termination\":true}],\"networks\":[{\"uuid\":\"662cae58-78aa-4488-84b9-d3a0f7968c16\"}],\"imageRef\":\"2153561a-d5ee-4ad0-8df3-f45932830e8d\",\"adminPass\":\"qweQWE123\",\"user_data\":\"Q29udGVudC1UeXBlOiBtdWx0aXBhcnQvbWl4ZWQ7IGJvdW5kYXJ5PSI9PT09PT09PT09PT09PT0yMzA5OTg0MDU5NzQzNzYyNDc1PT0iIApNSU1FLVZlcnNpb246IDEuMAoKLS09PT09PT09PT09PT09PT0yMzA5OTg0MDU5NzQzNzYyNDc1PT0KQ29udGVudC1UeXBlOiB0ZXh0L2Nsb3VkLWNvbmZpZzsgY2hhcnNldD0idXMtYXNjaWkiIApNSU1FLVZlcnNpb246IDEuMApDb250ZW50LVRyYW5zZmVyLUVuY29kaW5nOiA3Yml0CkNvbnRlbnQtRGlzcG9zaXRpb246IGF0dGFjaG1lbnQ7IGZpbGVuYW1lPSJzc2gtcHdhdXRoLXNjcmlwdC50eHQiIAoKI2Nsb3VkLWNvbmZpZwpkaXNhYmxlX3Jvb3Q6IGZhbHNlCnNzaF9wd2F1dGg6IHRydWUKcGFzc3dvcmQ6IHF3ZVFXRTEyMwoKLS09PT09PT09PT09PT09PT0yMzA5OTg0MDU5NzQzNzYyNDc1PT0KQ29udGVudC1UeXBlOiB0ZXh0L3gtc2hlbGxzY3JpcHQ7IGNoYXJzZXQ9InVzLWFzY2lpIiAKTUlNRS1WZXJzaW9uOiAxLjAKQ29udGVudC1UcmFuc2Zlci1FbmNvZGluZzogN2JpdApDb250ZW50LURpc3Bvc2l0aW9uOiBhdHRhY2htZW50OyBmaWxlbmFtZT0icGFzc3dkLXNjcmlwdC50eHQiIAoKIyEvYmluL3NoCmVjaG8gJ3Jvb3Q6cXdlUVdFMTIzJyB8IGNocGFzc3dkCgotLT09PT09PT09PT09PT09PTIzMDk5ODQwNTk3NDM3NjI0NzU9PQpDb250ZW50LVR5cGU6IHRleHQveC1zaGVsbHNjcmlwdDsgY2hhcnNldD0idXMtYXNjaWkiIApNSU1FLVZlcnNpb246IDEuMApDb250ZW50LVRyYW5zZmVyLUVuY29kaW5nOiA3Yml0CkNvbnRlbnQtRGlzcG9zaXRpb246IGF0dGFjaG1lbnQ7IGZpbGVuYW1lPSJlbmFibGUtZnMtY29sbGVjdG9yLnR4dCIgCgojIS9iaW4vc2gKcWVtdV9maWxlPSIvZXRjL3N5c2NvbmZpZy9xZW11LWdhIgppZiBbIC1mICR7cWVtdV9maWxlfSBdOyB0aGVuCiAgICBzZWQgLWkgLXIgInMvXiM/QkxBQ0tMSVNUX1JQQz0vI0JMQUNLTElTVF9SUEM9LyIgIiR7cWVtdV9maWxlfSIKICAgIGhhc19ncWE9JChzeXN0ZW1jdGwgbGlzdC11bml0cyAtLWZ1bGwgLWFsbCAtdCBzZXJ2aWNlIC0tcGxhaW4gfCBncmVwIC1vIHFlbXUtZ3Vlc3QtYWdlbnQuc2VydmljZSkKICAgIGlmIFtbIC1uICR7aGFzX2dxYX0gXV07IHRoZW4KICAgICAgICBzeXN0ZW1jdGwgcmVzdGFydCBxZW11LWd1ZXN0LWFnZW50LnNlcnZpY2UKICAgIGZpCmZpCgotLT09PT09PT09PT09PT09PTIzMDk5ODQwNTk3NDM3NjI0NzU9PS0t\"}}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```

其 `cURL (bash)` 请求如下：

```bash
curl 'https://172.20.154.250/api/openstack/regionone/nova/v2.1/servers' \
  -H 'Connection: keep-alive' \
  -H 'sec-ch-ua: "Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"' \
  -H 'pragma: no-cache' \
  -H 'Openstack-Api-Version: compute 2.79' \
  -H 'X-Openstack-Request-Id: req-eea89465-189f-4c06-8a42-065233c6d931' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'cache-control: no-cache' \
  -H 'X-Auth-Token: gAAAAABhQGCSgtdk-iC16-oeqB6s-99OkZ7MfZW7fyfmqwEYYn6SbHGZJxeCiBYZPYA8dEKZ1yXPLme-ytN6m3uGQFQY3LA3xp6gBIgfcIeehmn0BQH031Y3C3KPndEF1BdyV3McK3ZuJN8EpC4B0hFqFVmTWXhsCsdq_ajetDjZGEq1vB8CvXGcYNaRB0bevf6XQxHXC5BP' \
  -H 'DNT: 1' \
  -H 'sec-ch-ua-platform: "Windows"' \
  -H 'Origin: https://172.20.154.250' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://172.20.154.250/compute/instance/create' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cookie: csrftoken=BPdKTXavDBhhbnd9t6bzN055awB14JpsBov8jNkgaaEs8n4PPocNu56w8wFW2Wlj; session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlzdG9uZV90b2tlbiI6ImdBQUFBQUJoUUdDU2d0ZGstaUMxNi1vZXFCNnMtOTlPa1o3TWZaVzdmeWZtcXdFWVluNlNiSEdaSnhlQ2lCWVpQWUE4ZEVLWjF5WFBMbWUteXRONm0zdUdRRlFZM0xBM3hwNmdCSWdmY0llZWhtbjBCUUgwMzFZM0MzS1BuZEVGMUJkeVYzTWNLM1p1Sk44RXBDNEIwaEZxRlZtVFdYaHNDc2RxX2FqZXREalpHRXExdkI4Q3ZYR2NZTmFSQjBiZXZmNlhReEhYQzVCUCIsInJlZ2lvbiI6IlJlZ2lvbk9uZSIsImV4cCI6MTYzMTYxNDkzMywidXVpZCI6ImM4YjBjNjkwY2ViNDRjZjg5MzMwZGQ2NTE4ODNkZjJmIn0.kYohgTlWZmMFMy_HO0ZQavzhH_YUZ9U2SDZ5XinZ-4M' \
  --data-raw '{"server":{"security_groups":[{"name":"22e8def6-29cd-4bf5-ba8b-7339440dddde"}],"name":"demacia","flavorRef":"19cf6f69-ccb3-4c83-85f9-f2490b18fc48","availability_zone":"nova","block_device_mapping_v2":[{"boot_index":0,"uuid":"2153561a-d5ee-4ad0-8df3-f45932830e8d","source_type":"image","destination_type":"volume","volume_size":10,"volume_type":"6bb064b6-a240-48d2-ac75-d1bc9257d888","delete_on_termination":true}],"networks":[{"uuid":"662cae58-78aa-4488-84b9-d3a0f7968c16"}],"imageRef":"2153561a-d5ee-4ad0-8df3-f45932830e8d","adminPass":"qweQWE123","user_data":"Q29udGVudC1UeXBlOiBtdWx0aXBhcnQvbWl4ZWQ7IGJvdW5kYXJ5PSI9PT09PT09PT09PT09PT0yMzA5OTg0MDU5NzQzNzYyNDc1PT0iIApNSU1FLVZlcnNpb246IDEuMAoKLS09PT09PT09PT09PT09PT0yMzA5OTg0MDU5NzQzNzYyNDc1PT0KQ29udGVudC1UeXBlOiB0ZXh0L2Nsb3VkLWNvbmZpZzsgY2hhcnNldD0idXMtYXNjaWkiIApNSU1FLVZlcnNpb246IDEuMApDb250ZW50LVRyYW5zZmVyLUVuY29kaW5nOiA3Yml0CkNvbnRlbnQtRGlzcG9zaXRpb246IGF0dGFjaG1lbnQ7IGZpbGVuYW1lPSJzc2gtcHdhdXRoLXNjcmlwdC50eHQiIAoKI2Nsb3VkLWNvbmZpZwpkaXNhYmxlX3Jvb3Q6IGZhbHNlCnNzaF9wd2F1dGg6IHRydWUKcGFzc3dvcmQ6IHF3ZVFXRTEyMwoKLS09PT09PT09PT09PT09PT0yMzA5OTg0MDU5NzQzNzYyNDc1PT0KQ29udGVudC1UeXBlOiB0ZXh0L3gtc2hlbGxzY3JpcHQ7IGNoYXJzZXQ9InVzLWFzY2lpIiAKTUlNRS1WZXJzaW9uOiAxLjAKQ29udGVudC1UcmFuc2Zlci1FbmNvZGluZzogN2JpdApDb250ZW50LURpc3Bvc2l0aW9uOiBhdHRhY2htZW50OyBmaWxlbmFtZT0icGFzc3dkLXNjcmlwdC50eHQiIAoKIyEvYmluL3NoCmVjaG8gJ3Jvb3Q6cXdlUVdFMTIzJyB8IGNocGFzc3dkCgotLT09PT09PT09PT09PT09PTIzMDk5ODQwNTk3NDM3NjI0NzU9PQpDb250ZW50LVR5cGU6IHRleHQveC1zaGVsbHNjcmlwdDsgY2hhcnNldD0idXMtYXNjaWkiIApNSU1FLVZlcnNpb246IDEuMApDb250ZW50LVRyYW5zZmVyLUVuY29kaW5nOiA3Yml0CkNvbnRlbnQtRGlzcG9zaXRpb246IGF0dGFjaG1lbnQ7IGZpbGVuYW1lPSJlbmFibGUtZnMtY29sbGVjdG9yLnR4dCIgCgojIS9iaW4vc2gKcWVtdV9maWxlPSIvZXRjL3N5c2NvbmZpZy9xZW11LWdhIgppZiBbIC1mICR7cWVtdV9maWxlfSBdOyB0aGVuCiAgICBzZWQgLWkgLXIgInMvXiM/QkxBQ0tMSVNUX1JQQz0vI0JMQUNLTElTVF9SUEM9LyIgIiR7cWVtdV9maWxlfSIKICAgIGhhc19ncWE9JChzeXN0ZW1jdGwgbGlzdC11bml0cyAtLWZ1bGwgLWFsbCAtdCBzZXJ2aWNlIC0tcGxhaW4gfCBncmVwIC1vIHFlbXUtZ3Vlc3QtYWdlbnQuc2VydmljZSkKICAgIGlmIFtbIC1uICR7aGFzX2dxYX0gXV07IHRoZW4KICAgICAgICBzeXN0ZW1jdGwgcmVzdGFydCBxZW11LWd1ZXN0LWFnZW50LnNlcnZpY2UKICAgIGZpCmZpCgotLT09PT09PT09PT09PT09PTIzMDk5ODQwNTk3NDM3NjI0NzU9PS0t"}}' \
  --compressed \
  --insecure
```

## 关于 `user_data` 部分密码设置的问题

详见：[云主机密码登录相关功能](front-api/instance/password.md)

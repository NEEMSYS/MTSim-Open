# MTSim-Open
混合交通流管控策略仿真开放测试平台；Mixed Traffic Simulation Open Platform
## :fire: 目录
- 1.**[Introduction](#jump_1)**
- 2.**[快速开始](#jump_2)**
  - 2.1拉取代码 
  - 2.2编写流水线
  - 2.3配置服务器
- 3.**[项目说明](#jump_3)**
  - 3.1 
  - 3.2
  - 3.3
<a id="jump_1"></a>
## 📌1 Introction
> 说明：为什么要使用云原生构建（CNB）去集成项目？
1. 它利用 Docker 生态对环境、缓存、插件等进行抽象，通过声明式的语法，帮助开发者以更酷的方式构建软件。
2. 节约了服务器内存，不需要单独部署 Jenkins。（Jenkins内存占用较多）
3. 方便管理，代码和部署放在同一个地方，同时也支持其他的工作协同。

> 说明：为什么需要搞持续化集成？先说一说不使用持续集成前的使用场景：
1. 编写好代码代码后，使用 `npm build` 编辑成一个dist 文件夹
2. 打开 宝塔/ssh 连接，把dist变成一个压缩包，然后上传
3. 到指定目录去解压缩
这样非常的耗费时间，而且容易出错。经常不小心移动到了别的目录，或者需要快速迭代的，经常一天好打好几次包，这样的效率就太低下了。
> 持续化集成化后的使用步骤：
1. 编写到代码代码后，本地测试通过了，上传到 git。
2. 自动化处理 过几分钟就可以访问了

<a id="jump_2"></a>
## 📌2 快速开始
### 2.1 拉取代码
需将项目代码拉取到[云原生构建平台](https://cnb.cool/) 
  - `nginx.conf`文件修改。
```
location ~* /media/ {
            proxy_pass http://{后端代码所在服务器的ip地址};
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
```
  - `settings`文件修改：用到的mysql、redis相关配置的ip地址，都改成容器名。
<img width="708" height="307" alt="image" src="https://github.com/user-attachments/assets/a41212e3-c57c-4954-b71a-7c72cc8299c0" />

```java
git clone <本项目git地址>
```
### 2.2 编写流水线
即 **cnb.yml 文件**，根据要求修改端口号、ip地址、制品库等。
例如启动Django容器时，修改场景文件挂载地址，定义容器网络和容器名。
```
docker run -d -p 8000:8000 \
-v /medias:/app/media \
-v /results:/app/media/files/result \
-v /userresults:/app/media/files/userresult \
--network=myapp-network \
--name django-app \
${CNB_DOCKER_REGISTRY}/${CNB_REPO_SLUG_LOWERCASE}/${DOCKER_IMAGE_NAME1}:${DOCKER_IMAGE_VERSION}
```
为方便管理修改配置，还需配置文件 `react-ssh-secret.yml`
```
REMOTE_HOST: 101.37.80.39 //服务器的ip地址
REMOTE_USERNAME: root  //服务器用户名
REMOTE_PORT: 22    //端口号
VUE_CONTEXT: ./front       # Vue项目根目录
DOCKER_IMAGE_NAME: vue-app  # 镜像名
DOCKER_IMAGE_NAME1: django-app
DOCKER_IMAGE_VERSION: ${CNB_COMMIT}  # 使用CNB提交哈希作为标签
DOCKERFILE_PATH: ./front/Dockerfile  # 显式指定Dockerfile路径
DOCKERFILE_PATH1: ./back/Dockerfile  # 显式指定Dockerfile路径
DOCKER_BUILD_CONTEXT: .    # 构建上下文为项目根目录
//ssh登陆凭据
PRIVATE_KEY: |
    -----BEGIN RSA PRIVATE KEY-----
    ·····················
    -----END RSA PRIVATE KEY-----
```
### 2.3 配置服务器
服务器下载安装docker后，启动 **docker-compose.yml** 文件，启动`mysql`、`redis`、`celery`服务。
```
docker-compose up
```
最后云原生构建通过即可。
<a id="jump_3"></a>
## 📌3 项目说明

服务器上docker-compsoe用来启动mysql、redis服务，网络配置: myapp-network 允许容器之间通过自定义的桥接网络通信。  在流水线启动容器时加上参数： --network=root_myapp-network  ，表示在同一网络。

# MTSim-Open

### 混合交通流管控策略仿真开放测试平台

### Mixed Traffic Simulation Open Platform

![Django](https://img.shields.io/badge/Django-3.0-092E20?logo=django)

![Vue](https://img.shields.io/badge/Vue-2.6-4FC08D?logo=vue.js)

![SUMO](https://img.shields.io/badge/SUMO-1.22-FFCC00)

![Docker](https://img.shields.io/badge/Docker-containerized-2496ED?logo=docker)

![CI](https://img.shields.io/badge/CI-CNB%20云原生构建-1E90FF)

面向 CAV / HDV 混合交通流的典型管控场景（直线、合流、分流、事故），提供**参数化场景库 + 容器化策略评测 + 实时排行榜**的在线仿真测试环境。用户只需把算法封装成 Docker 镜像并填写镜像 ID，平台即可在云端批量跑完整个场景库，回传多维指标评分。

---

## 🔥 目录

- [1. Introduction](#-1-introduction)
- [2. 快速开始](#-2-快速开始)
  - [2.1 拉取代码](#21-拉取代码)
  - [2.2 编写流水线](#22-编写流水线)
  - [2.3 配置服务器](#23-配置服务器)
- [3. 项目说明](#-3-项目说明)
  - [3.1 系统架构与技术栈](#31-系统架构与技术栈)
  - [3.2 场景库与镜像规范](#32-场景库与镜像规范)
  - [3.3 评测流程与评分机制](#33-评测流程与评分机制)
- [4. 常见问题](#-4-常见问题)
- [5. 安全须知](#-5-安全须知)

---

## 📌 1 Introduction
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

---

## 📌 2 快速开始

### 2.1 拉取代码

需将项目代码拉取到[云原生构建平台](https://cnb.cool/) 

```bash
git clone <本项目 git 地址>
```

拉取后需要先改两处配置，否则容器之间互相访问不到：

**① `nginx.conf` 修改** —— 把 `/media/` 的 `proxy_pass` 指向后端代码所在服务器的 IP：

```nginx
location ~* /media/ {
    proxy_pass http://{后端代码所在服务器的ip地址};
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

**② `settings.py` 修改** —— 用到的 MySQL、Redis 相关配置的 IP 地址，都改成**容器名**：
<img width="708" height="307" alt="image" src="https://github.com/user-attachments/assets/a41212e3-c57c-4954-b71a-7c72cc8299c0" />

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django_03_04",
        "USER": "root",
        "PASSWORD": "******",
        "HOST": "mysql",      # 容器名，不要写 127.0.0.1
        "PORT": "3306",
    }
}
```

Redis 同理，写成容器名：

```python
broker_url = 'redis://redis:6379/15'
result_backend = 'redis://redis:6379/14'
```

> 改完 `settings.py` 记得重新构建镜像。容器里的配置是打包在镜像内的，只改宿主机文件、不重建镜像的话，线上跑的还是旧配置。

---

### 2.2 编写流水线

即 `cnb.yml` 文件，根据要求修改端口号、IP 地址、制品库等。例如启动 Django 容器时，修改场景文件挂载地址，定义容器网络和容器名：

```bash
docker run -d -p 8000:8000 \
  -v /medias:/app/media \
  -v /results:/app/media/files/result \
  -v /userresults:/app/media/files/userresult \
  --network=myapp-network \
  --name django-app \
  ${CNB_DOCKER_REGISTRY}/${CNB_REPO_SLUG_LOWERCASE}/${DOCKER_IMAGE_NAME1}:${DOCKER_IMAGE_VERSION}
```

三个挂载点分别对应平台的三类文件，**少挂一个就会丢结果**：

| 宿主机目录          | 容器内路径                         | 存什么                        |
| -------------- | ----------------------------- | -------------------------- |
| `/medias`      | `/app/media`                  | 场景库、比赛试卷、用户自定义场景           |
| `/results`     | `/app/media/files/result`     | 比赛测评的 tripinfo XML 与汇总 CSV |
| `/userresults` | `/app/media/files/userresult` | 自定义场景测评的结果文件               |

为方便管理修改配置，还需配置文件 `react-ssh-secret.yml`：

```yaml
REMOTE_HOST: 101.37.80.39          # 服务器的 ip 地址
REMOTE_USERNAME: root              # 服务器用户名
REMOTE_PORT: 22                    # 端口号

VUE_CONTEXT: ./front               # Vue 项目根目录
DOCKER_IMAGE_NAME: vue-app         # 镜像名
DOCKER_IMAGE_NAME1: django-app
DOCKER_IMAGE_VERSION: ${CNB_COMMIT}    # 使用 CNB 提交哈希作为标签
DOCKERFILE_PATH: ./front/Dockerfile    # 显式指定 Dockerfile 路径
DOCKERFILE_PATH1: ./back/Dockerfile    # 显式指定 Dockerfile 路径
DOCKER_BUILD_CONTEXT: .                # 构建上下文为项目根目录

# ssh 登陆凭据
PRIVATE_KEY: |
  -----BEGIN RSA PRIVATE KEY-----
  ·····················
  -----END RSA PRIVATE KEY-----
```

流水线本身分五段，顺序不能乱：

```
检出
 → 安装依赖（front: npm install）
 → 构建产物（front: npm run build）
 → 构建并推送 vue / django 两个镜像
 → SSH 到服务器重启容器
```

用 `${CNB_COMMIT}` 而不是 `latest` 作为镜像 tag，好处是每次部署都能精确回溯到某一次提交；配合部署前的 `docker rm -f 旧容器`，可以做到"不残留、可回滚"。

---

### 2.3 配置服务器

服务器下载安装 Docker 后，启动 `docker-compose.yml` 文件，启动 MySQL、Redis、Celery 服务：

```bash
docker compose up -d
```

最后云原生构建通过即可。

启动前先在宿主机把数据目录建好，否则容器会以 root 身份自动创建，之后宿主机上的非 root 用户就没有写权限了：

```bash
mkdir -p /medias /results /userresults /sumo_scenarios /userscenarios
```

服务器上的目录结构大致如下（红圈处为与评测强相关的目录）：
<img width="553" height="207" alt="服务器端文件结构" src="https://github.com/user-attachments/assets/2813c361-9165-4fe2-8806-70bd949201f1" />

- `results/` —— 比赛测评结果，内部按 `用户名/时间/output` 分层
- `userresults/` —— 自定义场景测评结果，结构同上
- `userscenarios/` —— 用户生成的场景，按 `用户名/type_xx/lanes_n/penetration_p%density_d` 分层
- `sumo_scenarios/` —— 系统预置场景库，按 `type_xx/lanes_n/vehsPerHour_n/penetration_n` 分层
- `medias/` —— Django 的 `MEDIA_ROOT`，比赛试卷、场景说明文档等上传文件

> 注意区分两类挂载：`sumo_scenarios` 与 `userscenarios` 是**挂进用户 Docker 容器**的（容器内路径 `/scenarios`，只读）；`results` 与 `userresults` 是**容器写出的目的地**（容器内路径 `/results`、`/userresults`，可写）。这层映射在 `back/MyCelery/DockerId/config.py` 里配置。

---

## 📌 3 项目说明

服务器上 `docker-compose` 用来启动 MySQL、Redis 服务，网络配置为 `myapp-network`，允许容器之间通过自定义的桥接网络通信。在流水线启动容器时加上参数 `--network=root_myapp-network`，表示在同一网络（CNB 会自动给项目网络加 `root_` 前缀，具体以服务器上 `docker network ls` 的输出为准）。

### 3.1 系统架构与技术栈

#### 技术栈

| 层次   | 选型                                               | 作用                |
| ---- | ------------------------------------------------ | ----------------- |
| 前端   | Vue 2.6 + Vue Router + Vuex + Element UI + Axios | 单页应用，无刷新交互        |
| 后端   | Django 3.0 + Django REST framework 3.11          | 业务接口、ORM、后台管理     |
| 鉴权   | djangorestframework-jwt                          | 无状态 Token，有效期 7 天 |
| 异步任务 | Celery 5.0 + Redis                               | 仿真任务排队、削峰填谷       |
| 实时通信 | Django Channels 3                                | 排行榜 WebSocket 推送  |
| 数据库  | MySQL 8.0                                        | 用户、比赛、作品、场景元数据    |
| 仿真引擎 | SUMO + TraCI 1.22                                | 微观交通流仿真           |
| 容器化  | Docker + Docker SDK for Python                   | 用户策略环境隔离与资源限额     |
| 远程同步 | paramiko（SFTP）                                   | 场景文件本地生成 → 云端同步   |

#### 模块划分

后端按业务域拆成三个 app，职责边界清晰：

| 模块          | 位置                | 职责                             |
| ----------- | ----------------- | ------------------------------ |
| `user`      | `back/user/`      | 注册、登录、JWT 签发、资料维护、改密           |
| `scenarios` | `back/scenarios/` | 场景库模型、序列化、多条件筛选、分页             |
| `game`      | `back/game/`      | 比赛、报名、作品提交、仿真触发、评分、排行榜、自定义场景生成 |
| `MyCelery`  | `back/MyCelery/`  | Celery 实例、Docker 任务、结果解析与打分    |

四个关键设计点：

1. **任务解耦**：`/api/run/` 里只做参数校验和 `Run.delay()` 投递，立刻返回 `{"status": "success"}`。仿真跑十分钟也不会拖垮 Web 进程。
2. **环境隔离**：用户策略跑在自己的 Docker 镜像里，依赖版本冲突、异常代码都在容器边界内被挡住（配合资源限额）。
3. **状态外置**：容器完全无状态，场景和结果全部通过 volume 挂载，容器销毁不影响任何数据。
4. **结果回流**：Celery Worker 解析结果、写库后，通过 `channel_layer.group_send("grades", ...)` 广播，前端表格无需轮询。

#### 目录结构

```
MTSim-Open/
├── back/                       # Django 后端
│   ├── django_03_04/           # settings / urls / asgi / routing
│   ├── user/                   # 用户模块
│   ├── scenarios/              # 场景库模块
│   ├── game/                   # 比赛、作品、评分、排行、场景生成
│   │   ├── views.py            # run_container / userrun_container / GenerateScenarioView
│   │   └── consumer.py         # 排行榜 WebSocket
│   ├── MyCelery/
│   │   ├── main.py             # Celery 实例
│   │   ├── config.py           # broker / backend
│   │   └── DockerId/
│   │       ├── config.py       # DOCKER_CONFIG：宿主机、配额、挂载目录
│   │       └── tasks.py        # Run / userRun / 指标解析 / 评分
│   ├── media/                  # 上传文件与结果
│   ├── Dockerfile
│   └── manage.py
├── front/                      # Vue 前端
│   ├── src/views/              # 首页/场景/比赛/我的比赛/作品/排行/个人中心
│   ├── src/layout/             # 布局与导航
│   ├── src/router/             # 路由表
│   ├── src/store/              # Vuex + sessionStorage 持久化
│   ├── src/plugins/            # axios 拦截器、Element UI
│   ├── nginx.conf
│   └── Dockerfile
├── sumo-lab/                   # 比赛场景的镜像模板
│   ├── main.py                 # TraCI 批量仿真入口
│   ├── Dockerfile              # ubuntu:22.04 + sumo + traci
│   └── requirements.txt
├── sumo-user/                  # 自定义场景的镜像模板（五层目录）
├── sumo_scenarios/             # 系统预置场景库
├── docker-compose.txt          # MySQL + Redis 编排
├── requirements.txt
└── cnb.yml                     # 流水线
```

### 3.2 场景库与镜像规范

#### 场景目录规范

场景库用**四级目录树**编码参数，路径本身就是元数据，不需要额外查表：

```
sumo_scenarios/
└── type_{场景类型}/
    └── lanes_{车道数}/
        └── vehsPerHour{车流量}/
            └── penetration_{渗透率}/
                ├── xxx.net.xml        # 路网拓扑
                ├── routes.rou.xml     # 车辆流与车辆类型定义
                └── xxx.sumocfg        # 仿真配置（net + rou + 起止时间 + 步长）
```

| 前缀              | 含义                   | 取值                 |
| --------------- | -------------------- | ------------------ |
| `type_SD`       | 直线路段（Straight）       | lanes_2 / 3 / 4    |
| `type_MS`       | 合流区（Merge，含 ramp 路网） | lanes_3 / 4        |
| `type_DS`       | 分流区（Diverge）         | lanes_3 / 4        |
| `type_AS`       | 事故路段（Accident）       | lanes_2 / 3 / 4    |
| `lanes_N`       | 车道数量                 | 2 ~ 4              |
| `vehsPerHour`   | 每小时到达车辆数             | 1500 / 2000 / 2500 |
| `penetration_N` | CAV 渗透率（%）           | 0, 10, 20 … 100    |

容器内的 `main.py` 靠 `glob` 逐层遍历这棵树来枚举全部参数组合，所以**目录命名必须严格符合上表**。少一层、拼错一个下划线，场景就会被静默跳过（日志里只会看到"发现 0 个场景"）。

#### 车辆模型

| 类型  | 跟驰模型   | 关键参数                                              |
| --- | ------ | ------------------------------------------------- |
| HDV | Krauss | `tau=1.5s`、`maxaccel=2.6`、`decel=4`、`maxspeed=33` |
| CAV | CACC   | `tau=0.8s`、`maxaccel=2.6`、`decel=5`、`maxspeed=33` |

`GenerateScenarioView` 按"总密度 × 渗透率"拆分 CAV / HDV 数量，动态生成 `.rou.xml`：

```python
cav_count = int(density * penetration / 100)
hdv_count = density - cav_count
```

#### 用户自定义场景

用户在页面上选场景类型（`straight` / `intersection`）、车道数、渗透率、车辆密度，后端按**五层目录**生成，比系统场景库多一层用户名做隔离：

```
media/user_scenarios/{username}/type_{type}/lanes_{n}/penetration_{p}%/density_{d}veh_hour/
    ├── {type}.net.xml      # 从模板库复制
    ├── {type}.rou.xml      # 按 CAV/HDV 数量生成
    └── demo1.sumocfg
```

本地生成后通过 SFTP 同步到云端 `/userscenarios`，保持同样的层级，等待容器挂载。参数范围约束：车道数 1~~6、渗透率 0~~100%、密度 50~2000 veh/hour。

#### 用户镜像契约

平台不关心镜像内部怎么实现，只要求满足以下四点，否则评测会失败或得 0 分：

1. 入口执行 `main.py`，接受平台传入的参数：  
   `--scenario_type=xxx --username=xxx --add_time=xxx --workers=N`（自定义场景额外带 `--seed=N`）
2. 场景目录从 `/scenarios` 读（只读挂载），结果目录写到 `/results` 或 `/userresults`（可写挂载）
3. 仿真输出的 XML 放在 `/{results|userresults}/{username}/{add_time}/output/` 下，平铺或嵌套均可（解析时用 `**/*.xml` 递归）
4. 文件名符合 `{config名}_seed{N}.xml`，解析器靠下划线后半段取随机种子

`sumo-lab/` 与 `sumo-user/` 就是可直接改的模板：

```bash
cd sumo-lab
docker build -t your-repo/your-strategy:v1 .
docker push your-repo/your-strategy:v1
```

提交时在平台填写 `your-repo/your-strategy:v1` 即可。

### 3.3 评测流程与评分机制



#### 结果指标

从 SUMO 的 `tripinfo.xml` 逐车提取，再聚合成场景级指标：

| 指标     | 字段               | 含义                          |
| ------ | ---------------- | --------------------------- |
| 平均时间损失 | `AVGTimeLoss`    | 因减速/停车产生的额外时间（s）            |
| 平均等待时间 | `AvgWaitingTime` | 怠速等待时长（s）                   |
| 平均旅行时间 | `AvgTravelTime`  | 全程行驶时长（s）                   |
| 平均延误   | `AvgDelay`       | `departDelay + timeLoss`（s） |
| 平均速度   | `AvgSpeed`       | 到达速度均值 × 3.6（km/h）          |
| 车辆数    | `VehicleCount`   | 参与统计的车辆总数                   |
| 随机种子   | `RandomSeed`     | 保证实验可复现                     |

汇总后的 CSV 形如：

```csv
ConfigPath,AVGTimeLoss,AvgWaitingTime,AvgTravelTime,AvgDelay,AvgSpeed,VehicleCount,RandomSeed
demo1.sumocfg,12.34,8.76,59.89,16.42,88.31,3600,seed_43
```

#### 评分模型

采用**双向归一化 + 加权求和**的百分制评分：

```
score_i = Σ ( w_k · normalize(x_k) ) × 100
normalize(v) = clamp((v - min) / (max - min), 0, 1)
```

- **越小越优**：时间损失、等待时间、旅行时间、延误 → 正向归一化
- **越大越优**：平均速度 → `reverse=True`，取 `1 - normalize`
- 最终得分为各场景得分的算术平均，保留两位小数

当前的基准值与权重（`calculate_score`）：

| 指标               | 基准值 | 权重  | 方向   |
| ---------------- | --- | --- | ---- |
| `AVGTimeLoss`    | 0   | 0.2 | 越小越好 |
| `AvgWaitingTime` | 0   | 0.2 | 越小越好 |
| `AvgTravelTime`  | 160 | 0.2 | 越小越好 |
| `AvgDelay`       | 4   | 0.2 | 越小越好 |
| `AvgSpeed`       | 126 | 0.2 | 越大越好 |

> 论文中针对合流 / 分流 / 事故场景设计了差异化权重（例如事故场景把 TTC 类安全指标权重提到 50%）。当前代码落地的是默认等权版本，`calculate_score()` 的注释里已经预留了"按场景类型走不同打分函数"的入口——后续加场景差异化打分只改这一个函数，不必动任务链路。

#### 资源公平性

多用户同时提交时，三层防护保证谁也别抢光谁：

| 层次   | 机制                                                               | 参数位置                                       |
| ---- | ---------------------------------------------------------------- | ------------------------------------------ |
| 任务准入 | `queue.Queue(maxsize=4)`，满则阻塞                                    | `game/views.py: max_concurrent_containers` |
| 容器资源 | `cpu_period / cpu_quota`（1.5 核）、`mem_limit=1g`、`cpuset_cpus=0-1` | `MyCelery/DockerId/config.py`              |
| 场景并行 | 容器内 `ProcessPoolExecutor(max_workers=N)`                         | `--workers` 参数                             |

#### 主要接口

| 方法       | 路径                                     | 说明                        |
| -------- | -------------------------------------- | ------------------------- |
| POST     | `/jwt-auth/`                           | 登录，返回 token + 用户信息 + 报名记录 |
| POST     | `/register/`                           | 注册                        |
| GET/PUT  | `/userinfo/{id}/`                      | 用户资料                      |
| PATCH    | `/update-pwd/`                         | 修改密码                      |
| GET      | `/scenarios/`                          | 场景库分页列表                   |
| GET      | `/filterScenarios/?formInlines={json}` | 按类型 / 车道 / 流量 / 渗透率筛选     |
| GET      | `/competition/`                        | 比赛列表                      |
| GET/POST | `/participant/`                        | 报名                        |
| GET      | `/grades/`                             | 排行榜（按分数倒序，每页 10 条）        |
| GET      | `/myWorks/?username=`                  | 我的作品                      |
| POST     | `/submitWorks/`                        | 提交比赛作品                    |
| POST     | `/run/`                                | 触发比赛场景异步测评                |
| POST     | `/generate_scenario/`                  | 生成自定义场景并同步云端              |
| POST     | `/usersubmitWorks/`                    | 提交自定义场景作品                 |
| POST     | `/userrun/`                            | 触发自定义场景异步测评               |
| GET      | `/userWorks/?username=`                | 我的自定义场景作品                 |
| WS       | `ws://{host}/ws/grades`                | 排行榜实时推送                   |

前端开发态在 `vue.config.js` 里配了 `/api` 代理与 `pathRewrite`，所以页面统一以 `/api/xxx/` 调用，生产态由 Nginx 转发。

---

## 📌 4 常见问题

**Q1：提交后排行榜一直没有分数？**  
按顺序排查：Celery Worker 在线？→ Redis 连通？→ Docker Daemon 2375 可达？→ 镜像能否以给定参数启动？Worker 日志出现 `Starting container with CPU time limiting...` 说明任务已进入执行阶段。

**Q2：容器跑了但 `score` 为空？**  
多半是结果路径没对上。任务期望在 `media/files/result/{username}/{time}/output` 下找到 XML；如果容器写到了别处，`process_xml_results` 会得到空结果集。

**Q3：`UploadWorks.objects.get()` 抛 `DoesNotExist`？**  
`add_time` 在数据库和容器参数中格式必须一致（平台会把 `:` 和空格替换成 `-`）。前端提交的字符串与 `/api/run/` 传入的必须是同一份值。

**Q4：排行榜只在部分用户那里刷新？**  
`CHANNEL_LAYERS` 目前是 `InMemoryChannelLayer`，只在单进程内有效。多 worker 部署必须换 `channels_redis`，否则组消息无法跨进程投递。

**Q5：改了 `settings.py` 但线上没生效？**  
容器里的 `settings.py` 来自镜像，不是宿主机文件。改完必须重新构建并推送镜像，再重启容器。

**Q6：本地没有 SUMO 能跑通吗？**  
可以。平台本身不依赖本地 SUMO，仿真发生在用户镜像内部。只有需要验证场景文件时，才需本地装 SUMO 打开 `.sumocfg`。

---

## 📌 5 安全须知

本仓库投产前请务必处理以下几点：

1. **凭据硬编码**：`settings.py` 的 `SECRET_KEY` / 数据库密码、`DockerId/config.py` 里的服务器账号密码、`GenerateScenarioView` 内的 `SERVER_CONFIG` 都是明文，应迁移到环境变量或密钥管理服务（CNB 的 secret 机制可直接用）。
2. **`DEBUG = True` 且 `ALLOWED_HOSTS = ['*']`**：仅适合开发，生产必须关闭 DEBUG 并限定主机。
3. **Docker Daemon 裸奔 2375**：无 TLS 的远程 Docker API 等同于服务器 root 权限，应启用 TLS 双向认证或改用受限的 socket-proxy。
4. **CSRF 中间件被注释**：为前后端分离调试便利而关闭，生产环境应重新启用。
5. **容器逃逸风险**：用户镜像以 `network=host` 高权限启动，应增加镜像白名单审核、`--read-only`、`cap_drop`、非 root 用户运行等加固。

---

## 参考

- SUMO 官方文档：<https://sumo.dlr.de/docs/index.html>
- TraCI 文档：<https://sumo.dlr.de/docs/TraCI.html>
- TraCI Python API：<https://sumo.dlr.de/pydoc/traci.html>
- Django REST framework：<https://www.django-rest-framework.org/>
- Celery：<https://docs.celeryq.dev/>
- CNB 云原生构建：<https://cnb.cool/>

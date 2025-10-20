# 基础镜像
FROM ubuntu:22.04

# 环境变量
ENV DEBIAN_FRONTEND=noninteractive

# 安装必要的软件包
RUN apt-get update && apt-get install -y \
    sumo sumo-tools sumo-doc \
    python3 python3-pip \
    tar && \
    apt-get clean

# 创建工作目录
WORKDIR /app

# 拷贝 SUMO 的配置文件和其他必要的文件到容器中
COPY ./path_to_sumo_files /app

# 暴露需要的端口（根据需求修改）
EXPOSE 8080

# 设置容器启动命令
CMD ["sumo", "-c", "path_to_config_file.sumocfg"]

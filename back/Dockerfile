# 使用官方 Python 镜像作为基础镜像
FROM python:3.7.6

# 配置时区和镜像源
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置容器内工作目录为 /app
WORKDIR /app

# 复制项目依赖文件（ requirements.txt 在 back 目录下）
COPY back/requirements.txt .

# 安装 Python 依赖
# 安装依赖，设置超时参数
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# 复制整个 back 目录到容器（此时构建上下文是根目录，back/ 是相对路径）
COPY back/ .

# 暴露 Django 默认端口
EXPOSE 8000

# 启动命令（修正版）

RUN chmod +x start.sh
CMD ["./start.sh"]
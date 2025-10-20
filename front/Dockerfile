FROM nginx:latest

# 删除默认配置（可选）
RUN rm -rf /etc/nginx/conf.d/

# 复制自定义配置
COPY front/nginx.conf /etc/nginx/nginx.conf

# 复制静态文件
COPY front/dist/ /usr/share/nginx/html
COPY back/media  /app/media
EXPOSE 80
# 覆盖 Entrypoint 以跳过默认配置加载
ENTRYPOINT ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]
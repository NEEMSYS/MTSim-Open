#!/bin/bash
#python manage.py makemigrations
#python manage.py migrate
# 启动 Celery 后台运行
python manage.py migrate &

celery -A MyCelery.main worker -l info -P gevent &

# 启动 Django 开发服务器
python manage.py runserver 0.0.0.0:8000

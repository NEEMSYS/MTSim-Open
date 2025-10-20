from celery import Celery
import os
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_03_04.settings')

app = Celery('MyCelery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 确保每个任务完成后关闭数据库连接
@app.task(bind=True)
def debug_task(self):
    connection.close()
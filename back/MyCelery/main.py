import os
import sys
from celery import Celery
from celery.signals import worker_shutdown

# 添加项目根目录到 Python 路径
#sys.path.append('d:\\bishe_4 - c')

# 设置 Django 的默认配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_03_04.settings')

# 创建 Celery 实例
app = Celery("RunDocker")

# 加载配置
app.config_from_object("MyCelery.config")

# 自动发现任务
app.autodiscover_tasks(["MyCelery.DockerId",])

# 确保 Django 应用已加载
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# 启动 Celery 的命令 Celery -A MyCelery.main worker -l info -P gevent
# 启动 Redis redis-server.exe redis.windows.conf
# 使用 flower 来监控 Celery Celery -A MyCelery.main flower --broker=redis://localhost:6379/15 --address=127.0.0.1 --result_backend=redis://localhost:6379/

# 在app创建后添加
app.conf.update(
    task_acks_late=True,  # 确保任务执行完成后再确认
    worker_prefetch_multiplier=1,  # 避免预取任务导致竞争
    broker_connection_max_retries=None,  # 无限重试连接
)

@worker_shutdown.connect
def shutdown_handler(**kwargs):
    """Properly close Redis connections on worker shutdown"""
    from celery import current_app
    if current_app.connection_for_write():
        current_app.connection_for_write().close()
    if current_app.connection_for_read():
        current_app.connection_for_read().close()

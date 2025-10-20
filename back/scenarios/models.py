import re
from uuid import uuid4

from django.db import models
import os
from functools import partial  # 新增导入

# 保持原有函数定义完全不变
def dynamic_path(instance, filename, file_type):
    params = [
        sanitize_filename(instance.types),
        f"Lan_{instance.lines}",
        f"vehsPerHour_{instance.vehsPerHour}",
        f"penetration_{instance.permeability.replace('%', 'p')}"
    ]
    unique_id = uuid4().hex[:8]
    new_filename = f"{'_'.join(params)}_{filename}"
    return os.path.join(
        Scenarios.BASE_PATH,
        instance.types,
        f"Lan_{instance.lines}",
        f"vehsPerHour_{instance.vehsPerHour}",
        file_type,
        new_filename
    )


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|%^]', '_', name).strip()

class Scenarios(models.Model):
    # 保持原有字段定义完全不变
    name = models.CharField(verbose_name="文件名称", max_length=30)
    types = models.CharField(verbose_name="路网类型", max_length=10)
    lines = models.IntegerField(verbose_name="车道数量")
    vehsPerHour = models.IntegerField(verbose_name="车辆数量")
    permeability = models.CharField(verbose_name="渗透率", max_length=5)
    BASE_PATH = "files/scenarios"

    # 修改点：使用partial替代lambda
    file = models.FileField(
        upload_to=partial(dynamic_path, file_type='file')  # 关键修改
    )
    docfile = models.FileField(
        upload_to=partial(dynamic_path, file_type='doc') # 关键修改)  # 关键修改
    )

    class Meta:
        db_table = "scenarios"
        verbose_name = "场景库"





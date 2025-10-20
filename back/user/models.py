from django.db import models
from django.contrib.auth.models import AbstractUser, User


class UserInfo(models.Model):
    """ 用户信息类 """
    name = models.CharField("姓名", max_length=20, default="")
    # 一对一关联字段
    user = models.OneToOneField(User, verbose_name="用户", on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('m', '男'),
        ('g', '女')
    )
    age = models.IntegerField("年龄", default=0)
    gender = models.CharField("性别", max_length=1, choices=GENDER_CHOICES, default="")
    email = models.CharField(verbose_name="邮箱", max_length=23)

    class Meta:
        ordering = ['id']
        db_table = "userinfo"
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

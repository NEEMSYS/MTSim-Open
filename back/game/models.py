from django.db import models
from django.contrib.auth.models import AbstractUser, User
from datetime import datetime

# Create your models here.

class Competition(models.Model):
    """
    比赛信息表
    """
    # 比赛名称
    name = models.CharField(max_length=100, unique=True)
    # 比赛信息
    description = models.TextField()
    # 比赛试卷
    exam_paper = models.FileField(upload_to='files/competition_papers/')
    # 新增比赛类型字段
    scenario_type = models.CharField(max_length=50, default='type1', verbose_name='场景类型')

    scenario_des = models.CharField(verbose_name="场景描述", max_length=200, default='直线路段')
    def __str__(self):
        return self.name


class Attend(models.Model):
    """
    比赛报名表
    """
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition,on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        db_table = "attend"
        verbose_name = '比赛报名信息'
        verbose_name_plural = verbose_name

class UploadWorks(models.Model):
    """
    提交作品表
    """
    # 将用户的用户名保存下来
    username = models.ForeignKey(User, verbose_name="用户名", to_field="username", on_delete=models.CASCADE)

    # 用户提交作品的时候也必须提交的相应的比赛的名字，作为比赛表中的外键
    competition_name = models.ForeignKey(Competition, verbose_name="比赛名称", to_field="name", on_delete=models.CASCADE)

    # 保存镜像ID
    dockerId = models.CharField(verbose_name="镜像ID", max_length =200)

    add_time = models.CharField(verbose_name="上传时间",max_length=30)

    # 保存分数, 分数取重复提交的最大值
    score = models.FloatField(verbose_name="成绩", blank=True,null=True)

    scenario_type = models.CharField(
        max_length=20,
        verbose_name='场景类型',
        default='type1'  # 添加默认值
    )

    # 保存镜像ID
    scenario_des = models.CharField(verbose_name="场景描述", max_length =200,default='直线路段')
    # 保存结果的文件
    result_file = models.FileField(blank=True, upload_to='files/result')  # 结果文件保存在服务器上，这是服务器的地址

    class Meta:
        ordering = ['id']
        db_table = "uploadworks"
        verbose_name = "提交作品表"


class userUploadWorks(models.Model):
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    scenario_type = models.CharField(max_length=50, verbose_name='自定义场景类型')
    competition_name = models.CharField(max_length=100, verbose_name='自定义比赛名称')
    dockerId = models.CharField(max_length=200, verbose_name='镜像ID')
    result_file = models.FileField(blank=True,upload_to='files/userresult')
    add_time = models.CharField(verbose_name="上传时间",max_length=30)
    score = models.FloatField(verbose_name='得分', null=True, blank=True)

    class Meta:
        verbose_name = '自定义场景作品'
        verbose_name_plural = verbose_name
        db_table = "useruploadworks"




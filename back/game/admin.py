from django.contrib import admin
from django.shortcuts import render, redirect
from MyCelery.DockerId.config import DOCKER_CONFIG
from game.models import Competition, Attend, UploadWorks  # 添加DockerConfig到imports

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "exam_paper", "scenario_type","scenario_des"]
    search_fields = ['name']  # 添加搜索功能
    list_filter = ['scenario_type']  # 添加过滤器


class AttendAdmin(admin.ModelAdmin):
    list_display = ["user", "competition"]


class UploadWorksAdmin(admin.ModelAdmin):
    list_display = ["username", "competition_name", "add_time", "score", "scenario_type","scenario_des"]
    search_fields = ['username']  # 添加搜索功能
    list_filter = ['scenario_type']  # 添加过滤器
    # 修改装饰器为旧版兼容方式
    def scenario_type(self, obj):
        return obj.competition_name.scenario_type

    def scenario_des(self, obj):
        return obj.competition_name.scenario_des
    scenario_type.admin_order_field = 'competition_name__scenario_type'
    scenario_type.short_description = '比赛类型'


# 注册到admin
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Attend, AttendAdmin)
admin.site.register(UploadWorks, UploadWorksAdmin)

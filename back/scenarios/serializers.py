from rest_framework import serializers
from scenarios.models import Scenarios
from django.conf import settings

class ScenariosSerializers(serializers.ModelSerializer):
    # 新增自定义文件字段处理
    file = serializers.SerializerMethodField()
    docfile=serializers.SerializerMethodField()
    class Meta:
        model = Scenarios
        fields = ["name", "types", "lines", "vehsPerHour", "permeability", "file","docfile"]

    def get_file(self, obj):
        # 方法1：硬编码生产环境地址（快速修复）
        production_host = "http://114.215.195.207:8000"
        return f"{production_host}{obj.file.url}"
    def get_docfile(self, obj):
        # 方法1：硬编码生产环境地址（快速修复）
        production_host = "http://114.215.195.207:8000"
        return f"{production_host}{obj.docfile.url}"
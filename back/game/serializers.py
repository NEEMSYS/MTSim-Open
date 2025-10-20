from rest_framework import serializers
from game.models import Competition, Attend, UploadWorks, userUploadWorks


# 比赛信息序列化
class CompetitionSerializers(serializers.ModelSerializer):
    # exam_paper=serializers.FileField()
    class Meta:
        model = Competition
        fields = '__all__'
    # def get_exam_paper(self, obj):
    #     # 方法1：硬编码生产环境地址（快速修复）
    #     production_host = "http://114.215.195.207:8000"
    #     return f"{production_host}{obj.exam_paper.url}"

# 存储比赛报名信息
class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attend
        fields = '__all__'


# 存储提交的信息
class SubmitWorksSerializer(serializers.ModelSerializer):
    competition_name = serializers.PrimaryKeyRelatedField(queryset=Competition.objects.all())
    scenario_type = serializers.CharField(read_only=True, source='competition_name.scenario_type')
    scenario_des= serializers.CharField(read_only=True, source='competition_name.scenario_des')
    class Meta:
        model = UploadWorks
        fields = ['username', 'competition_name', 'scenario_type', 'dockerId', 'add_time', 'score','scenario_des','scenario_des','result_file']


#存储用户自定义场景信息
class userSubmitWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = userUploadWorks
        fields = '__all__'

# 排行榜信息 指定序列化器 WorksSerializer，负责将数据库模型转换为 JSON 格式
class WorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadWorks
        fields = ['username','add_time', 'score']

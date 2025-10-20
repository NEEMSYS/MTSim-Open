import errno
import json
import shutil
import stat
import zipfile
from venv import logger
import logging
logger = logging.getLogger(__name__)

# 可选：配置日志格式（在Django settings.py中更推荐）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
from django.http import FileResponse, Http404, JsonResponse
from rest_framework.response import Response

from django_03_04 import settings
from game.models import Competition, Attend, UploadWorks, userUploadWorks
from game.serializers import CompetitionSerializers, ParticipantSerializer, SubmitWorksSerializer, WorksSerializer, \
    userSubmitWorksSerializer
from rest_framework import viewsets, status
from django.shortcuts import HttpResponse
from MyCelery.DockerId.tasks import Run, userRun, RemoteFileExplorer
import re
import os
from celery.result import AsyncResult
from scenarios.views import MypageNumberPagination
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.files.base import ContentFile
# 在文件顶部添加
from game.models import Competition
import threading
import queue

# 比赛信息
class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializers


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    保存报名信息，将报名信息返回给用户，保存到sessionStorage
    """
    queryset = Attend.objects.all()
    serializer_class = ParticipantSerializer
    # 查询集 competition_id = self.request.query_params.get('competition_id', None)
    # queryset = Participant.objects.filter(competition_id=pk)


class SubmitWorksViewSet(viewsets.ModelViewSet):
    """
    保存提交的信息
    """
    queryset = UploadWorks.objects.all()
    print("111")
    serializer_class = SubmitWorksSerializer
    print("222")

    def create(self, request, *args, **kwargs):
        print("Request data:", request.data)
        try:
            # 创建数据副本
            data = request.data.copy()

            # 获取比赛对象
            competition_name = data.get('competition_name')
            if competition_name:
                competition = Competition.objects.get(name=competition_name)
                data['competition_name'] = competition.id
                data['scenario_type'] = competition.scenario_type
                data['scenario_des'] = competition.scenario_des
            # 使用修改后的数据创建实例
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            self.trigger_grades_update()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Create error:", str(e))
            raise

    def trigger_grades_update(self):
        channel_layer = get_channel_layer()

        # 从数据库中获取最新成绩，并序列化
        queryset = UploadWorks.objects.all().order_by('-score')
        # print("排序后数据:", list(queryset.values_list('id', 'score')))

        serializer = WorksSerializer(queryset, many=True)
        grades = serializer.data

        # 发送消息到grades组
        async_to_sync(channel_layer.group_send)(
            "grades",
            {
                "type": "send_updated_grades",
                "grades": grades
            }
        )
        print("trigger_grades_update")


max_concurrent_containers = 4  # 设定最大并发容器数
container_queue = queue.Queue(maxsize=max_concurrent_containers)
def run_container(request):
    # 异步任务
    if request.method == 'POST':
        data = json.loads(request.body)
        # 从数据中获取 dockerId
        docker_id = data.get('dockerId')
        username = data.get('username')
        add_time = data.get('add_time')
        competition_name = data.get('competition_name')  # Add this line

        # 添加用户自定义场景
        userscenario_type = data.get('scenario_type')
        custom_scenario = data.get('custom_scenario')

        competition = Competition.objects.get(name=competition_name)

        scenario_type = competition.scenario_type
        # 启动任务并获取结果
        if container_queue.full():
            print("达到最大并发限制，等待一个容器完成")
            container_queue.get()  # 等待一个容器完成
        container_queue.put(docker_id)
        result = Run.delay(docker_id, username, add_time, scenario_type)
        return JsonResponse({
            'status': 'success'
        })
    else:
        return HttpResponse("Task start failed")



# 测试自定义场景

class userSubmitWorksViewSet(viewsets.ModelViewSet):
    """
    保存提交的信息
    """
    queryset = userUploadWorks.objects.all()
    serializer_class = userSubmitWorksSerializer

    def create(self, request, *args, **kwargs):
        # 调用父类的create方法来创建新的SubmitWorks实例
        print("Request data:", request.data)
        response = super().create(request, *args, **kwargs)
        # 创建成功后返回排行榜的信息
        return response


def userrun_container(request):
    # 异步任务
    if request.method == 'POST':
        data = json.loads(request.body)
        # 从数据中获取 dockerId
        docker_id = data.get('dockerId')
        username = data.get('username')
        add_time = data.get('add_time')
        competition_name = data.get('competition_name')
        scenario_type = data.get('scenario_type')
        # 启动任务并获取结果
        if container_queue.full():
            print("达到最大并发限制，等待一个容器完成")
            container_queue.get()  # 等待一个容器完成
        container_queue.put(docker_id)
        result = userRun.delay(docker_id, username, add_time, scenario_type)
        return JsonResponse({
            'status': 'success'
        })
    else:
        return HttpResponse("Task start failed")


# 排行榜信息
class GradesViewset(viewsets.ModelViewSet):
    """
    排行榜视图集
    提供比赛成绩的查询、分页及排序功能

    核心功能：
    1. 根据用户提交的算法得分（score）动态排序
    2. 支持分页查询（默认每页10条，可自定义）
    3. 仅返回有效比赛记录（过滤无效或未完成数据）
    """

    # 数据库查询集定义
    # queryset = UploadWorks.objects.all().order_by('-score')
    queryset = UploadWorks.objects.filter(score__isnull=False).order_by('-score')  # 过滤掉无分数的记录
    # 按score降序排列（高分在前）
    # -score 表示倒序排序（默认升序为 order_by('score')）

    # 序列化器配置
    serializer_class = WorksSerializer  # 使用WorksSerializer处理数据序列化

    # 分页配置
    pagination_class = MypageNumberPagination  # 自定义分页类，继承自rest_framework.pagination.PageNumberPagination

    def list(self, request, *args, **kwargs):
        # 强制设置每页数量
        request.query_params._mutable = True
        request.query_params['page_size'] = 10  # 设置为10条每页
        request.query_params._mutable = False
        return super().list(request, *args, **kwargs)


class MyWorksViewset(viewsets.ModelViewSet):
    serializer_class = SubmitWorksSerializer
    queryset = UploadWorks.objects.none()

    def get_queryset(self):
        username = self.request.query_params.get("username")
        return UploadWorks.objects.filter(username=username)


class UserCustomWorksViewset(viewsets.ModelViewSet):
    serializer_class = userSubmitWorksSerializer
    queryset = userUploadWorks.objects.none()

    def get_queryset(self):
        username = self.request.query_params.get("username")
        return userUploadWorks.objects.filter(username=username)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import random
from pathlib import Path
from django.conf import settings


class GenerateScenarioView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        scenario_type = data.get('type')
        lanes = data.get('lanes', 2)
        penetration = data.get('penetration', 50)
        density = data.get('density', 200)

        # 场景类型与基础文件映射（根据车道数量）
        SCENARIO_MAP = {
            'straight': {
                2: 'SD_2.net.xml',
                3: 'SD_3.net.xml',
                4: 'SD_4.net.xml'
            },
            'intersection': {
                2: 'intersection_2.net.xml',
                3: 'intersection_3.net.xml',
                4: 'intersection_4.net.xml'
            }
        }

        # 检查场景类型和车道数量是否有效
        if scenario_type not in SCENARIO_MAP or lanes not in SCENARIO_MAP[scenario_type]:
            return Response({
                'status': 'error',
                'message': f'不支持的场景类型或车道数量: {scenario_type} {lanes}车道'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 获取对应车道数量的net文件
        net_file = SCENARIO_MAP[scenario_type][lanes]

        # 计算CAV和HDV的车辆数
        cav_count = int(density * penetration / 100)
        hdv_count = density - cav_count
        # 生成rou.xml内容
        rou_content = f"""<?xml version="1.0" encoding="UTF-8"?>
        <routes>
            <vType carFollowModel="Krauss" decel="4" id="HDV" maxaccel="2.6" maxspeed="33" tau="1.5" vClass="passenger"/>
            <vType carFollowModel="CACC" decel="5" id="CAV" maxaccel="2.6" maxspeed="33" tau="0.8" vClass="private"/>
            <flow id="HDV-flow1" type="HDV" arrivalLane="current" begin="0" color="0,1,0" departLane="random" departSpeed="33" end="3600" from="E0" to="E1" vehsPerHour="{hdv_count}"/>
            <flow id="CAV-flow1" type="CAV" arrivalLane="current" begin="0" color="1,0,0" departLane="random" departSpeed="33" end="3600" from="E0" to="E1" vehsPerHour="{cav_count}"/>
        </routes>
                """

        # 本地目录生成
        scenario_dir = os.path.join(
            settings.MEDIA_ROOT,
            'user_scenarios',
            username,
            f"type_{scenario_type}",
            f"lanes_{lanes}",
            f"penetration_{penetration}%",
            f"density_{density}veh_hour"
        )
        os.makedirs(scenario_dir, exist_ok=True)
        print(scenario_dir)
        # 复制对应的net.xml文件
        net_file = SCENARIO_MAP[scenario_type][lanes]  # 正确：获取具体文件名
        src_net_path = os.path.join(settings.MEDIA_ROOT, 'files', net_file)
        dst_net_path = os.path.join(scenario_dir, f"{scenario_type}.net.xml")
        shutil.copy2(src_net_path, dst_net_path)

        # 保存rou.xml文件
        rou_path = os.path.join(scenario_dir, f"{scenario_type}.rou.xml")
        with open(rou_path, 'w') as f:
            f.write(rou_content)

        # 生成并保存sumocfg配置文件
        config_content = f"""
              <configuration>
                  <input>
                      <net-file value="{scenario_type}.net.xml"/>
                      <route-files value="{scenario_type}.rou.xml"/>
                  </input>
                  <time>
		              <begin value="0"/>
		                <end value ="3600"/>
		                <step-length value="0.5"/>
	              </time>
              </configuration>
              """
        config_path = os.path.join(scenario_dir, 'demo1.sumocfg')
        with open(config_path, 'w') as f:
            f.write(config_content)

        # 云端配置（保持不变）
        SERVER_CONFIG = {
            "host": "114.215.195.207",
            "port": 22,
            "username": "root",
            "password": "2580zjmZJM",
            "base_dir": "/userscenarios"
        }

        try:
            with RemoteFileExplorer(
                    host=SERVER_CONFIG["host"],
                    port=SERVER_CONFIG["port"],
                    username=SERVER_CONFIG["username"],
                    password=SERVER_CONFIG["password"],
                    base_dir=SERVER_CONFIG["base_dir"]
            ) as explorer:

                # 构建远程目录路径
                remote_dir = '/'.join([
                    SERVER_CONFIG["base_dir"],
                    username,
                    f"type_{scenario_type}",
                    f"lanes_{lanes}",
                    f"penetration_{penetration}%",
                    f"density_{density}veh_hour"
                ])
                print(remote_dir)

                # 分割远程目录并逐级创建
                dirs_to_create = remote_dir.split('/')
                current_path = ''
                for directory in dirs_to_create:
                    if not directory:
                        continue
                    current_path += '/' + directory
                    try:
                        # 尝试获取目录状态，若不存在则创建
                        explorer.sftp.stat(current_path)
                    except IOError:
                        try:
                            explorer.sftp.mkdir(current_path, mode=0o755)
                            print(f"创建远程目录成功: {current_path}")
                        except Exception as e:
                            logger.error(f"创建目录失败 {current_path}: {str(e)}")
                            raise

                # 上传sumo文件
                # 上传net.xml
                with open(dst_net_path, 'rb') as local_file:
                    explorer.sftp.putfo(local_file, f"{remote_dir}/{scenario_type}.net.xml")

                # 上传rou.xml
                with open(rou_path, 'rb') as local_file:
                    explorer.sftp.putfo(local_file, f"{remote_dir}/{scenario_type}.rou.xml")

                # 上传sumocfg配置文件
                with open(config_path, 'rb') as local_file:
                    explorer.sftp.putfo(local_file, f"{remote_dir}/demo1.sumocfg")


        except Exception as e:

            logger.error(f"上传失败: {str(e)}")

            return Response({

                'status': 'error',

                'message': f'上传到云端失败: {str(e)}'

            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'status': 'success',
            'scenario_id': os.path.basename(scenario_dir),
            'local_path': scenario_dir,
            'remote_path': remote_dir,
            'config': 'demo1.sumocfg',
            'parameters': {
                'type': scenario_type,
                'lanes': lanes,
                'penetration': f"{penetration}%",
                'density': f"{density}veh/hour"
            }
        }, status=status.HTTP_201_CREATED)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import random
from pathlib import Path
from django.conf import settings




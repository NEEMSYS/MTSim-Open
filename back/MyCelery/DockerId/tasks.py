# import random
# import re
import stat
# import time
# from stat import S_ISDIR
# import redis
# from celery.exceptions import Reject
# from celery.utils.time import timezone
# from celery.worker.state import requests
#
# from MyCelery.DockerId.config import DOCKER_CONFIG
# from MyCelery.main import app
# import docker
# import os
# import tarfile
# from io import BytesIO
# from celery import current_task
# from game.models import Competition
# from django.db import close_old_connections
#
# import sys
# from pathlib import Path
import random
import re
import sys
from pathlib import Path, PurePosixPath
# from celery.utils.time import timezone
# from celery.worker.state import requests
from celery import current_task
# from game.models import Competition
# from django.db import close_old_connections
import docker
import os
# import tarfile
# from io import BytesIO
from paramiko import Transport,SFTPClient, RSAKey
from MyCelery.DockerId.config import DOCKER_CONFIG
from MyCelery.main import app
from game.models import UploadWorks, userUploadWorks
from pathlib import PurePosixPath  # 用 PurePosixPath 替代 os.path
# from .redis_counter import RedisCounter  # 确保已导入
import pandas as pd
# 自动检测项目根目录
project_root = Path(__file__).resolve().parents[1]  # 根据实际层级调整
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 此处设置虚拟机上docker的端口 2375
# 修改 DockerClient 初始化
client = docker.DockerClient(
    base_url=DOCKER_CONFIG['host'],
    timeout=300  # 全局超时设置
)
# 此处设置虚拟机上docker的端口 2375


# 全局计数器
ainers = 0


class RemoteFileExplorer:
    def __init__(self, host, port, username, password=None, key_path=None, base_dir=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_path = key_path
        self.base_dir = base_dir
        self.sftp = None
        self.transport = None

    def __enter__(self):
        """进入上下文时建立连接"""
        try:
            self.transport = Transport((self.host, self.port))
            if self.key_path:
                private_key = RSAKey.from_private_key_file(self.key_path)
                self.transport.connect(username=self.username, pkey=private_key)
            else:
                self.transport.connect(username=self.username, password=self.password)
            self.sftp = SFTPClient.from_transport(self.transport)
            # 验证基础目录是否存在
            if self.base_dir and not self.sftp.stat(self.base_dir).st_mode | 0o40000:
                raise FileNotFoundError(f"基础目录不存在: {self.base_dir}")
            return self
        except Exception as e:
            self.close()
            raise RuntimeError(f"连接建立失败: {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时安全关闭连接"""
        try:
            if self.sftp:
                self.sftp.close()
        except:
            pass
        try:
            if self.transport:
                self.transport.close()
        except:
            pass
        # 清理资源
        self.sftp = None
        self.transport = None

    def find_scenarios(self, scenario_type=None):
        """获取服务器上的SUMO场景路径（使用SFTP协议）"""
        scenarios = []

        # 构建基础目录路径
        base_path = PurePosixPath(self.base_dir)

        try:
            # 获取基础目录下的所有条目
            dir_entries = self.sftp.listdir_attr(base_path.as_posix())
        except IOError as e:
            raise RuntimeError(f"无法访问基础目录: {str(e)}")

        for entry in dir_entries:
            # 只处理目录
            if not stat.S_ISDIR(entry.st_mode):
                continue

            # 构建完整路径
            scenario_dir = base_path / entry.filename

            # 如果指定了场景类型且不匹配则跳过
            if scenario_type and entry.filename != scenario_type:
                continue

            # 遍历需求目录（第二层）
            for demand_entry in self.sftp.listdir_attr(scenario_dir.as_posix()):
                if not stat.S_ISDIR(demand_entry.st_mode):
                    continue

                demand_path = scenario_dir / demand_entry.filename

                # 遍历渗透率目录（第三层）
                for pen_entry in self.sftp.listdir_attr(demand_path.as_posix()):
                    if not stat.S_ISDIR(pen_entry.st_mode):
                        continue

                    pen_path = demand_path / pen_entry.filename

                    # 查找配置文件
                    config_path = pen_path / 'demo1.sumocfg'
                    try:
                        self.sftp.stat(config_path.as_posix())
                    except IOError:
                        continue

                    # 收集有效场景
                    scenarios.append({
                        'type': entry.filename,  # 场景类型（第一层目录名）
                        'demand': demand_entry.filename,  # 需求文件名（第二层目录名）
                        'penetration': pen_entry.filename,  # 渗透率目录名（第三层）
                        'path': pen_path.as_posix(),  # 完整路径
                        'config': config_path.as_posix()  # 配置文件路径
                    })

        if not scenarios:
            return {
                'status': 'error',
                'message': '未找到包含demo1.sumocfg的有效场景'
            }

        return scenarios

    def find_user_scenarios(self, username=None):
        """
        查找用户自定义SUMO场景路径（五层目录结构）
        目录结构：用户名/场景类型/车道数/渗透率/场景密度
        """
        scenarios = []
        base_path = PurePosixPath(self.base_dir)

        try:
            # 获取基础目录下的所有条目
            dir_entries = self.sftp.listdir_attr(base_path.as_posix())
        except IOError as e:
            raise RuntimeError(f"无法访问基础目录: {str(e)}")

        for user_entry in dir_entries:
            # 只处理目录且匹配用户名
            if not stat.S_ISDIR(user_entry.st_mode) or (username and user_entry.filename != username):
                continue

            user_path = base_path / user_entry.filename

            # 遍历场景类型目录
            for type_entry in self.sftp.listdir_attr(user_path.as_posix()):
                if not stat.S_ISDIR(type_entry.st_mode):
                    continue
                type_path = user_path / type_entry.filename

                # 遍历车道数目录
                for lane_entry in self.sftp.listdir_attr(type_path.as_posix()):
                    if not stat.S_ISDIR(lane_entry.st_mode):
                        continue
                    lane_path = type_path / lane_entry.filename

                    # 遍历渗透率目录
                    for pen_entry in self.sftp.listdir_attr(lane_path.as_posix()):
                        if not stat.S_ISDIR(pen_entry.st_mode):
                            continue
                        pen_path = lane_path / pen_entry.filename

                        # 遍历场景密度目录
                        for density_entry in self.sftp.listdir_attr(pen_path.as_posix()):
                            if not stat.S_ISDIR(density_entry.st_mode):
                                continue
                            density_path = pen_path / density_entry.filename

                            # 验证配置文件
                            config_path = density_path / "demo1.sumocfg"
                            try:
                                self.sftp.stat(config_path.as_posix())
                            except IOError:
                                continue

                            # 收集有效场景
                            scenarios.append({
                                "username": user_entry.filename,  # 用户名来自目录名
                                "type": type_entry.filename,
                                "lanes": lane_entry.filename,
                                "penetration": pen_entry.filename,
                                "density": density_entry.filename,
                                "path": density_path.as_posix(),
                                "config": config_path.as_posix()
                            })

        # 最终校验
        if not scenarios:
            return {
                "status": "error",
                "message": "未找到包含demo1.sumocfg的有效场景"
            }

        return scenarios

HOST_DIR = '/results'
# 全局变量，用于记录当前运行的容器数量
current_containers = 0
from xml.etree import ElementTree as ET
import logging
logger = logging.getLogger(__name__)

# 可选：配置日志格式（在Django settings.py中更推荐）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
import csv
def parse_tripinfo(xml_path: Path):
    """解析tripinfo XML文件并提取指标"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        metrics = []

        for trip in root.findall('tripinfo'):
            # 提取核心字段
            duration = float(trip.get('duration', 0))  # 行驶时间（秒）
            time_loss = float(trip.get('timeLoss', 0))  # 时间损失（秒）
            waitingTime = float(trip.get('waitingTime', 0))  # 怠速时间（秒）
            depart_delay = float(trip.get('departDelay', 0))  # 出发延误（秒）

            # 计算复合指标
            total_delay = depart_delay + time_loss  # 总延误
            speed = float(trip.get('arrivalSpeed', 0))  # 到达速度

            metrics.append({
                'duration': duration,
                'time_loss': time_loss,
                'waitingTime': waitingTime,
                'total_delay': total_delay,
                'speed': speed,
                'vehicle_id': trip.get('id')
            })

        return metrics

    except ET.ParseError as e:
        logger.error(f"XML解析失败: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"处理文件 {xml_path} 失败: {str(e)}")
        return []

def process_xml_results(results_dir: str, username: str, add_time: str):
        """生成包含完整指标的CSV文件"""
        input_dir = Path(results_dir)
        # 创建用户专属结果目录（容器内路径）
        user_results_dir = Path(f"media/files/result/{username}/{add_time}/results")
        user_results_dir.mkdir(parents=True, exist_ok=True)

        all_metrics = []

        for xml_file in input_dir.glob("**/*.xml"):
            try:
                metrics = parse_tripinfo(xml_file)
                if not metrics:
                    continue

                # 计算指标
                results = calculate_metrics(metrics)

                # 转换为CSV行数据
                file_metrics = {
                    "ConfigPath": xml_file.parent.name,
                    # "TrafficFlow": results['traffic_flow'],
                    "AVGTimeLoss": results['AVGTimeLoss'],
                    "AvgWaitingTime": results['AvgWaitingTime'],
                    "AvgTravelTime": results['avg_travel_time'],
                    "AvgDelay": results['avg_delay'],
                    "AvgSpeed": results['avg_speed'],
                    "VehicleCount": len(metrics),
                    "RandomSeed": xml_file.stem.split('_')[1]
                }

                all_metrics.append(file_metrics)

            except Exception as e:
                logger.error(f"处理文件 {xml_file} 失败: {str(e)}")

        # 写入CSV
        if all_metrics:
            with open(user_results_dir / "simulation_results.csv", 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "ConfigPath", "AVGTimeLoss", "AvgWaitingTime",
                    "AvgTravelTime", "AvgDelay", "AvgSpeed",
                    "VehicleCount", "RandomSeed"
                ])
                writer.writeheader()
                writer.writerows(all_metrics)
                # 写入最终结果
        output_csv=user_results_dir / "simulation_results.csv"
        print(output_csv)
        return str(output_csv)


def process_xml_results_user(results_dir: str, username: str, add_time: str):
    """生成包含完整指标的CSV文件"""
    input_dir = Path(results_dir)
    # 创建用户专属结果目录（容器内路径）
    user_results_dir = Path(f"media/files/userresult/{username}/{add_time}/results")
    user_results_dir.mkdir(parents=True, exist_ok=True)

    all_metrics = []

    for xml_file in input_dir.glob("**/*.xml"):
        try:
            metrics = parse_tripinfo(xml_file)
            if not metrics:
                continue

            # 计算指标
            results = calculate_metrics(metrics)

            # 转换为CSV行数据
            file_metrics = {
                "ConfigPath": xml_file.parent.name,
                #"TrafficFlow": results['traffic_flow'],
                "AVGTimeLoss": results['AVGTimeLoss'],
                "AvgWaitingTime": results['AvgWaitingTime'],
                "AvgTravelTime": results['avg_travel_time'],
                "AvgDelay": results['avg_delay'],
                "AvgSpeed": results['avg_speed'],
                "VehicleCount": len(metrics),
                "RandomSeed": xml_file.stem.split('_')[1]
            }

            all_metrics.append(file_metrics)

        except Exception as e:
            logger.error(f"处理文件 {xml_file} 失败: {str(e)}")

    # 写入CSV
    if all_metrics:
        with open(user_results_dir / "simulation_results.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "ConfigPath", "AVGTimeLoss", "AvgWaitingTime",
                "AvgTravelTime", "AvgDelay", "AvgSpeed",
                "VehicleCount", "RandomSeed"
            ])
            writer.writeheader()
            writer.writerows(all_metrics)
            # 写入最终结果
    output_csv = user_results_dir / "simulation_results.csv"
    print(output_csv)
    return str(output_csv)
@app.task
def Run(dockerid, username, add_time, scenario_type):
    """ 获取到的docker id 在docker中运行"""
    print("111")
    # 为用户创建一个唯一的文件夹
    #user_dir = os.path.join(HOST_DIR, str(username), str(add_time))
    result_dir=('/results')
    print("222")
    #os.makedirs(user_dir,exist_ok=True)
    print("333")

    """ 带CPU时间片控制的容器运行 """
    workers=DOCKER_CONFIG['workers']
    try:
        print("Starting container with CPU time limiting...")
        # 计算CPU时间片参数（核心数转换为时间片配额）
        cpu_limit = DOCKER_CONFIG['cpu_limit']
        cpu_period = 100000  # 100ms（必须与系统cgroup周期对齐）;设置每个容器进程的调度周期
        cpu_quota = int(cpu_period * cpu_limit)  # 计算时间片配额;设置在每个周期内容器能使用的 CPU 时间
        time = add_time.replace(":", "-")
        time = time.replace(" ", "-")
        container = client.containers.run(
            dockerid,
            volumes={
                DOCKER_CONFIG['scenario_dir']: {'bind': '/scenarios', 'mode': 'ro'},
                result_dir: {'bind': '/results', 'mode': 'rw'}
            },
            detach=True,
            network_mode='host',
            command=[f"--scenario_type={scenario_type}", f"--username={username}", f"--add_time={time}",f"--workers={workers}"],

            # 正确参数配置
            cpu_period=cpu_period,
            cpu_quota=cpu_quota,
            mem_limit=DOCKER_CONFIG['memory_limit'],

            # （可选）
            cpuset_cpus="0-1",  # 绑定物理核心（假设4核服务器）,限制容器运行在指定的CPU核心,表示容器中的进程可以在 CPU-0、CPU-1、CPU-2和CPU-3 上执行。
            cpu_shares=int(1024 * cpu_limit), # 设置CPU优先级,通过cpu share可以设置容器使用CPU的优先级。
        )

        print(f"Container {container.id} started with CPU limit: {cpu_limit} cores")
        container.wait()
        logs = container.logs().decode('utf-8')
        # score=calculate_score(logs)

        # 在服务器上，容器挂载，这个地址要改
        user_dir = f"media/files/result/{username}/{time}"  # 格式: alice/20240508_1530
        # 新增结果处理
        xml_results_dir = f"{user_dir}/output"  # 容器内输出路径映射到宿主机
        csv_path = process_xml_results(xml_results_dir, username, time)
        # 修改评分计算方式
        # 读取CSV并计算评分
        df = pd.read_csv(csv_path)
        #指标都提取，计算分数的时候看不同的指标，根据场景类型字段写不同的calculate_score函数
        score = calculate_score(df)

        user = UploadWorks.objects.get(username=username, add_time=add_time)
        # 更新数据库
        user.score = score
        user.scenario_type = scenario_type
        #去掉media前缀
        user_dir1 = f"files/result/{username}/{time}"
        file_path = f"{user_dir1}/results/simulation_results.csv"
        user.result_file = file_path
        user.save(update_fields=['score', 'scenario_type', 'result_file'])  # 只更新必要字段
        return {
            'status': 'success',
            'score': score,
        }

    except docker.errors.APIError as e:
        return {'status': 'error', 'message': str(e)}

@app.task
def userRun(dockerid, username, add_time, scenario_type):
    """ 获取到的docker id 在docker中运行"""
    print("111")
    # 为用户创建一个唯一的文件夹
    # user_dir = os.path.join(HOST_DIR, str(username), str(add_time))
    result_dir = ('/userresults')
    print("222")
    # os.makedirs(user_dir,exist_ok=True)
    print("333")
    time = add_time.replace(":", "-")
    time = time.replace(" ", "-")
    """ 带CPU时间片控制的容器运行 """
    try:
        print("Starting container with CPU time limiting...")

        # 计算CPU时间片参数（核心数转换为时间片配额）
        cpu_limit = DOCKER_CONFIG['cpu_limit']
        cpu_period = 100000  # 100ms（必须与系统cgroup周期对齐）;设置每个容器进程的调度周期
        cpu_quota = int(cpu_period * cpu_limit)  # 计算时间片配额;设置在每个周期内容器能使用的 CPU 时间
        # 每次任务执行时动态生成种子
        seed = random.randint(0, 100)
        # 构造命令
        workers = DOCKER_CONFIG['workers']
        container = client.containers.run(
            dockerid,
            volumes={
                DOCKER_CONFIG['userscenario_dir']: {'bind': '/scenarios', 'mode': 'ro'},
                result_dir: {'bind': '/userresults', 'mode': 'rw'}
            },
            network='host',
            detach=True,
            command=[f"--username={username}", f"--add_time={time}", f"--scenario_type={scenario_type}",f"--seed={seed}", f"--workers={workers}"],
            # 正确参数配置
            cpu_period=cpu_period,
            cpu_quota=cpu_quota,
            mem_limit=DOCKER_CONFIG['memory_limit'],

            # （可选）
            cpuset_cpus="0-1",  # 绑定物理核心（假设4核服务器）,限制容器运行在指定的CPU核心,表示容器中的进程可以在 CPU-0、CPU-1、CPU-2和CPU-3 上执行。
            cpu_shares=int(1024 * cpu_limit),  # 设置CPU优先级,通过cpu share可以设置容器使用CPU的优先级。
        )

        print(f"Container {container.id} started with CPU limit: {cpu_limit} cores")
        container.wait()
        logs = container.logs().decode('utf-8')
        # score=calculate_score(logs)

        # 在服务器上，容器挂载，这个地址要改
        user_dir = f"media/files/userresult/{username}/{time}"  # 格式: alice/20240508_1530
        # 新增结果处理
        xml_results_dir = f"{user_dir}/output"  # 容器内输出路径映射到宿主机
        csv_path = process_xml_results_user(xml_results_dir, username, time)
        # 修改评分计算方式
        # 读取CSV并计算评分
        df = pd.read_csv(csv_path)
        # 指标都提取，计算分数的时候看不同的指标，根据场景类型字段写不同的calculate_score函数
        score = calculate_score(df)

        user = userUploadWorks.objects.get(username=username, add_time=add_time)
        # 更新数据库
        user.score = score
        user.scenario_type = scenario_type
        # 去掉media前缀
        user_dir1 = f"files/userresult/{username}/{time}"
        file_path = f"{user_dir1}/results/simulation_results.csv"
        user.result_file = file_path
        user.save(update_fields=['score', 'scenario_type', 'result_file'])  # 只更新必要字段

        return {
            'status': 'success',
            'score': score,
        }


    except docker.errors.APIError as e:
        return {'status': 'error', 'message': str(e)}



def calculate_metrics(metrics):
    """计算综合交通指标"""
    if not metrics:
        return {
            #'traffic_flow': 0,
            'AVGTimeLoss': 0,
            'AvgWaitingTime': 0,
            'avg_travel_time': 0,
            'avg_delay': 0,
            'avg_speed': 0
        }

    df = pd.DataFrame(metrics)

    # 交通流量（每小时通过车辆数）
    traffic_flow = len(df)

    # AVGTimeLoss（总排放时间 = ∑timeLoss）
    AVGTimeLoss = df['time_loss'].mean()

    # AvgWaitingTime（总怠速时间 = ∑waitingTime）
    AvgWaitingTime = df['waitingTime'].mean()

    # 平均旅行时间（秒）
    avg_travel_time = df['duration'].mean()

    # 平均延误（出发延误 + 行驶延误）
    avg_delay = df['total_delay'].mean()

    # 平均速度（km/h，假设1单位距离=1公里）
    valid_speeds = df[df['speed'] > 0]['speed']
    avg_speed = valid_speeds.mean() * 3.6 if not valid_speeds.empty else 0

    return {
        #'traffic_flow': traffic_flow,
        'AVGTimeLoss': round(AVGTimeLoss,2),
        'AvgWaitingTime': round(AvgWaitingTime,2),
        'avg_travel_time': round(avg_travel_time, 2),
        'avg_delay': round(avg_delay, 2),
        'avg_speed': round(avg_speed, 2)
    }


def calculate_score(df: pd.DataFrame) -> float:
    """基于多指标的加权评分系统"""
    # 基准值配置（可根据实际情况调整）
    BASE_VALUES = {
        #"TrafficFlow": 1200,  # 基准交通流量（辆/小时）
        "AVGTimeLoss": 0,  # 时间损失（减速、停车造成的延误）（秒）
        "AvgWaitingTime": 0,  # 等待时间（秒）
        "AvgTravelTime": 160,  # 基准行程时间（秒）
        "AvgDelay": 4,  # 基准延误（秒）
       "AvgSpeed": 126  # 基准速度（km/h）
    }

    # 权重配置（总和100%）
    WEIGHTS = {
       # "TrafficFlow": 0.15,
        "AVGTimeLoss": 0.2,
        "AvgWaitingTime": 0.2,
        "AvgTravelTime": 0.2,
        "AvgDelay": 0.2,
        "AvgSpeed": 0.2
    }

    scores = []

    for _, row in df.iterrows():
        try:
            # 方向处理：越小越好 vs 越大越好
            normalized = {
               # "TrafficFlow": normalize(row["TrafficFlow"], 0, BASE_VALUES["TrafficFlow"], reverse=True),
                "AVGTimeLoss": normalize(row["AVGTimeLoss"], 0, BASE_VALUES["AVGTimeLoss"]),
                "AvgWaitingTime": normalize(row["AvgWaitingTime"], 0, BASE_VALUES["AvgWaitingTime"]),
                "AvgTravelTime": normalize(row["AvgTravelTime"], 0, BASE_VALUES["AvgTravelTime"]),
                "AvgDelay": normalize(row["AvgDelay"], 0, BASE_VALUES["AvgDelay"]),
                "AvgSpeed": normalize(row["AvgSpeed"], 0, BASE_VALUES["AvgSpeed"], reverse=True)
            }

            # 加权计算
            total = (
                   # normalized["TrafficFlow"] * WEIGHTS["TrafficFlow"] +
                    normalized["AVGTimeLoss"] * WEIGHTS["AVGTimeLoss"] +
                    normalized["AvgWaitingTime"] * WEIGHTS["AvgWaitingTime"] +
                    normalized["AvgTravelTime"] * WEIGHTS["AvgTravelTime"] +
                    normalized["AvgDelay"] * WEIGHTS["AvgDelay"]+
                    normalized["AvgSpeed"] * WEIGHTS["AvgSpeed"]
            ) * 100  # 转换为百分制

            scores.append(total)

        except KeyError as e:
            logger.error(f"字段缺失: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"评分异常: {str(e)}")

    return round(sum(scores) / len(scores), 2) if scores else 0.0


def normalize(value, min_val, max_val, reverse=False):
    if min_val == max_val:
        return 0.5
    ratio = (value - min_val) / (max_val - min_val)
    ratio = min(max(ratio, 0), 1)  # 限制在[0,1]范围内
    return ratio if reverse else 1 - ratio
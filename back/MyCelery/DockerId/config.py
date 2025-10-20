DOCKER_CONFIG = {
    'host': 'tcp://114.215.195.207:2375',  # Docker连接地址
    #'max_concurrent_containers': 2,   # 最大并发容器数
    'workers': 4,                   #单用户并行场景数量
    'cpu_limit': 1.5,                # 默认CPU限制(核数)
    'cpu_period': 100000,  # CPU周期（微秒，默认100ms）
    'cpu_quota': 100000,  # CPU配额（微秒）= 1核 * 100000周期
    'memory_limit': '1g',            # 默认内存限制
    'gpu_limit': 0,                 # GPU限制(0表示不使用)
    'remote_host': '114.215.195.207',
    "username": "root",
    "password": "2580zjmZJM",  # 或使用密钥
    "port": 22,
    'scenario_dir':'/sumo_scenarios',
    'userscenario_dir':'/userscenarios',
    'remote_base_dir': '/sumo_scenarios',
    'cgroup_parent': '/docker_fair_share'  # 自定义cgroup分组

}

# from redis import Redis
# from .redis_counter import RedisCounter

# # 在DOCKER_CONFIG后添加Redis配置
# REDIS_CLIENT = Redis.from_url(
#     'redis://localhost:6379/15',
#     socket_timeout=10,
#     socket_connect_timeout=5,
#     retry_on_timeout=True
# )

# 初始化Redis计数器
# REDIS_COUNTER = RedisCounter(
#     REDIS_CLIENT,
#     "docker_containers",
#     DOCKER_CONFIG['max_concurrent_containers']
# )
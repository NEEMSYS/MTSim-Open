""" 编写处理websocket的逻辑 """

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class GradeConsumer(WebsocketConsumer):

    def connect(self):
        print("开始连接")
        """ web浏览器的客户端发送请求, 建立连接"""
        self.accept()   # 接收客户端的连接请求
        # 将当前连接添加到名为"grades"的组中，这样当发送消息到这个组时，这个连接可以接收到消息
        async_to_sync(self.channel_layer.group_add)("grades",self.channel_name)

    def disconnect(self, close_code):
        # 当客户端断开WebSocket连接时调用此方法
        # 从名为”grades“的组中移除当前连接，这样他就不会接收到发送到改组的消息
        async_to_sync(self.channel_layer.group_discard)("grades", self.channel_name)

    def send_updated_grades(self, event):
        # 当收到一个类型为"send_updated_grades"的时间时调用此方法
        # 将事件中的"grades"数据(经过JSON序列化)发送给客户端
        self.send(text_data=json.dumps(event["grades"]))


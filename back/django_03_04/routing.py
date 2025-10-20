from game import consumer
from django.urls import path

websocket_urlpatterns =[
    path("ws/grades",consumer.GradeConsumer.as_asgi())
]
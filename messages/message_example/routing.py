from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from message.consumers import MessagesConsumer

application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(  #认证
        URLRouter([
                path('ws/<str:username>/',MessagesConsumer)  #相当于urls.py的作用，给这个websocket请求相应的Consumer处理
            ])
        )

    })
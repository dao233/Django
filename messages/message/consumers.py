import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MessagesConsumer(AsyncWebsocketConsumer):
    '''处理私信websocket请求'''
    async def connect(self):
        if self.scope['user'].is_anonymous:
            # 拒绝匿名用户连接
            await self.close()
        else:
            # 加入聊天组，以当前登录用户的用户名为组名，即self.scope['user'].username
            await self.channel_layer.group_add(self.scope['user'].username,self.channel_name)
            await self.accept()

    async def receive(self,text_data=None,bytes_data=None):
        '''接收到后端发来的私信'''
        print(text_data)
        await self.send(text_data=json.dumps(text_data))  #发送到接收用户

    async def disconnect(self,code):
        '''离开聊天组'''
        await self.channel_layer.group_discard(self.scope['user'].username,self.channel_name)

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .models import *

from asgiref.sync import async_to_sync,sync_to_async
from channels.layers import get_channel_layer

def message(request):
    '''用于返回主页'''
    return render(request,'message.html')

def login_(request):
    '''用于登录'''
    if request.method == 'GET':
        return render(request,'login.html')
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    if User.objects.filter(username=username):
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
            return redirect('message/')
    return render(request,'login.html')

def notes(request):
    '''用来显示用户列表'''
    username = request.user
    users = User.objects.filter(is_active=True).exclude(username=request.user).order_by('-last_login')
    # 上一句作用是筛选除自己外，is_active=True的用户，并以最后一次登录时间排序
    return render(request,'notes.html',locals())

def chat(request,username):
    if request.method == 'GET':
        '''处理get请求，返回两用户的聊天记录'''
        recipient = User.objects.get(username=username)
        sender = request.user
        qs_one = Message.objects.filter(sender=sender,recipient=recipient)  # A发送给B的信息
        qs_two = Message.objects.filter(sender=recipient,recipient=sender)  # B发送给A的信息
        all = qs_one.union(qs_two).order_by('created_at')  # 取查到的信息内容的并集，相当于他两的聊天记录
        return render(request,'chat.html',locals())
    else:
        recipient = User.objects.get(username=username)  # 消息接收者
        content = request.POST.get('content','')  # 消息内容
        sender = request.user  # 发送者
        msg = Message.objects.create(sender=sender,recipient=recipient,message=content)  # 把消息存储到数据库
        qs_one = Message.objects.filter(sender=sender,recipient=recipient)  # A发送给B的信息
        qs_two = Message.objects.filter(sender=recipient,recipient=sender)  # B发送给A的信息
        all = qs_one.union(qs_two).order_by('created_at')  # 取查到的信息内容的并集，相当于他两的聊天记录
        channel_layer = get_channel_layer()
        # get_channel_layer()函数获得的是当前的websocket连接所对应的consumer类对象的channel_layer
        payload = {
            'type':'receive',  # 这个type是有限制的，比如现在用到的就是cusumer的receive函数
            'message':content,  # 消息内容
            'sender':request.user.username,  # 发送者
            'created_at':str(msg.created_at)  # 创建时间
        }
        group_name = username  #这里用的是接收者的用户名为组名，每个用户在进入聊天框后就会自动进入以自己用户名为组名的group
        async_to_sync(channel_layer.group_send)(group_name, payload)
        #上一句是将channel_layer.group_send()从异步改为同步，正常的写法是channel_layer.group_send(group_name, payload)
        return render(request,'chat.html',locals())





from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User,related_name='sent_messages',on_delete=models.SET_NULL,blank=True,null=True,verbose_name='发送者')
    recipient = models.ForeignKey(User,related_name='receive_messages',on_delete=models.SET_NULL,blank=True,null=True,verbose_name='接收者')
    message = models.TextField(blank=True,null=True,verbose_name='内容')
    unread = models.BooleanField(default=True,db_index=True,verbose_name='是否未读')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

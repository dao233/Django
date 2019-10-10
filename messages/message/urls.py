from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.login_,name='login'),
    path('message/',views.message,name='message'),
    path('notes/',views.notes,name='notes'),
    path('chat/<username>',views.chat,name='chat'),
]
from django.urls import path
from django.conf.urls import url, include 

from . import views

app_name = 'chat'

urlpatterns = [
    path('',views.login_request, name='login_request'),
    path('home',views.home, name='home'),
    path('register',views.register, name='register'),
    path('logout_request',views.logout_request, name='logout_request'),
    path('chats/<path:link>', views.get_messages, name='get_messages'),
]
from django.conf.urls import url, include
from api import views

urlpatterns = [
    url('^entry', views.entry),
    #  获取总服务器信息
    url(r'^asset/', views.asset),
]

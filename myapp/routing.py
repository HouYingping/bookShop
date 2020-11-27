from django.urls import re_path,path
from . import ChatConsumer

#routing.py路由文件跟django的url.py功能类似，语法也一样，
# 意思就是访问ws/chat/都交给ChatConsumer处理
websocket_urlpatterns=[
    # re_path(r'^ws/chat/(?P<room_name>[^/]+)/$',ChatConsumer),
    path('ws/chat/',ChatConsumer)
]
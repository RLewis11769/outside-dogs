""" Add routing patterns for websocket connected to consumer """
from django.urls import re_path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    # Not sure if regex necessary - ws/chat/room_name
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer()),
]

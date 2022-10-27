from django.urls import re_path
from . import consumers,win_chat

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/win_chat/(?P<room_name>\w+)/$", win_chat.ChatConsumer.as_asgi()),
]

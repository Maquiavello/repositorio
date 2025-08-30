from django.urls import re_path, path
from . import consumers
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/sala/<sala_id>/', ChatConsumer.as_asgi()),
]
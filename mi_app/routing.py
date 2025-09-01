from django.urls import re_path

from mi_app.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/sala/(?P<sala_id>\w+)/$', ChatConsumer.as_asgi()),
]
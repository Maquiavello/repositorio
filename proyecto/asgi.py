import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import mi_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')


application = ProtocolTypeRouter({
    'http': get_asgi_application(),  # Maneja HTTP (incluyendo archivos estáticos)
    'websocket': AuthMiddlewareStack(
        URLRouter(mi_app.routing.websocket_urlpatterns)
    )  # Tu configuración de WebSockets aquí
})
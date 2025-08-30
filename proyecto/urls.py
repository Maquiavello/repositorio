from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'message': '¡API Django con Channels funcionando!',
        'status': 'OK',
        'websocket': 'wss://mi-app-1-2wv9.onrender.com/ws/sala/{sala_id}/',  # ← URL CORREGIDA
        'endpoint_example': 'wss://mi-app-1-2wv9.onrender.com/ws/sala/1/',   # ← Ejemplo con ID
        'endpoints': {
            'admin': '/admin/',
            'api': '/app/'
        }
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('app/', include('mi_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
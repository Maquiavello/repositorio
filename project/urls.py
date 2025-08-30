from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # Importa RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirige la URL raíz a la URL de inicio de sesión.
    path('', RedirectView.as_view(url='/app/login/', permanent=True)),
    path('app/', include('mi_app.urls')),
]

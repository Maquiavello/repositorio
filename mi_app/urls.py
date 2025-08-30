from django.urls import path
from mi_app import views
from .views import Sala, usuarios

urlpatterns = [
    path('registro', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('menu/', views.menu, name='menu'),
    path('sala/<int:sala_id>/', views.sala, name="sala"),
    path('logout/', views.logout, name='logout'),
]
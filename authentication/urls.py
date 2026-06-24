from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('validar/', views.validar_registro, name='validar'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
]
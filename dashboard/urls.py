from django.urls import path
from . import views

# Espacio de nombres para evitar colisiones con otras apps
app_name = 'dashboard'

urlpatterns = [
    path('', views.panel_control, name='panel'),
    path('modificar/<int:consulta_id>/', views.panel_modificar, name='modificar'),
    path('eliminar/<int:consulta_id>/', views.panel_eliminar, name='eliminar'),
]
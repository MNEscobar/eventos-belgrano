from django.urls import path
from . import views

# Espacio de nombres para evitar colisiones con otras apps
app_name = 'dashboard'

urlpatterns = [
    path('', views.panel_control, name='panel'),
]
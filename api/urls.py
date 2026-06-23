from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # La ruta final será /api/consultas/
    path('consultas/', views.ConsultaListAPIView.as_view(), name='consultas_list'),
]
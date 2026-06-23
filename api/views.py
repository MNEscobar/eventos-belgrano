from rest_framework import generics
from eventos_app.models import Consulta
from .serializers import ConsultaSerializer

class ConsultaListAPIView(generics.ListAPIView):
    """
    Endpoint que devuelve la lista de todas las consultas registradas en formato JSON.
    """
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
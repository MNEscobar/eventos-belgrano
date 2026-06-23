from rest_framework import serializers
from eventos_app.models import Consulta

class ConsultaSerializer(serializers.ModelSerializer):
    # Campos calculados legibles para que la API sea más fácil de consumir
    tipo_evento_display = serializers.CharField(source='get_tipo_evento_display', read_only=True)
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)

    class Meta:
        model = Consulta
        # Enviamos todos los campos, más nuestros campos legibles
        fields = [
            'id', 'nombre', 'email', 'telefono', 
            'tipo_evento', 'tipo_evento_display', 
            'fecha_evento', 'cantidad_invitados', 
            'mensaje', 'categoria', 'categoria_display', 
            'fecha_consulta'
        ]
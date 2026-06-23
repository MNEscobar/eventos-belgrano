from django.contrib import admin
from .models import Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'tipo_evento', 'fecha_evento', 'cantidad_invitados', 'fecha_consulta']
    list_filter = ['tipo_evento', 'fecha_consulta']
    search_fields = ['nombre', 'email']
    readonly_fields = ['fecha_consulta']
    ordering = ['-fecha_consulta']

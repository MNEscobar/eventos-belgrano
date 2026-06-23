from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from eventos_app.models import Consulta

@login_required(login_url='authentication:login')

def panel_control(request):
    """Vista principal del panel de administración a medida."""
    # Obtenemos todas las consultas ordenadas
    consultas = Consulta.objects.all()
    
    # Calculamos las estadísticas
    total_consultas = consultas.count()
    total_comercial = consultas.filter(categoria='Comercial').count()
    total_tecnica = consultas.filter(categoria='Técnica').count()
    total_rrhh = consultas.filter(categoria='RRHH').count()
    total_general = consultas.filter(categoria='General').count()

    context = {
        'titulo': 'Panel de Control - Estadísticas',
        'consultas': consultas,
        'stats': {
            'total': total_consultas,
            'comercial': total_comercial,
            'tecnica': total_tecnica,
            'rrhh': total_rrhh,
            'general': total_general,
        }
    }
    return render(request, 'dashboard/panel.html', context)
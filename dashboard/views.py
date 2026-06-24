from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from eventos_app.models import Consulta
from eventos_app.forms import ConsultaForm

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

@login_required(login_url='authentication:login')
def panel_modificar(request, consulta_id):
    """Permite editar una solicitud existente."""
    consulta = get_object_or_404(Consulta, id=consulta_id)

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()  # el save() del modelo re-clasifica automáticamente (ver punto 1)
            messages.success(request, 'La solicitud se actualizó correctamente.')
            return redirect('dashboard:panel')
        else:
            messages.error(request, 'Revisá los datos ingresados.')
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, 'dashboard/modificar.html', {'form': form, 'consulta': consulta})

@login_required(login_url='authentication:login')
def panel_eliminar(request, consulta_id):
    """Pide confirmación y elimina la solicitud (solo vía POST, nunca por GET)."""
    consulta = get_object_or_404(Consulta, id=consulta_id)

    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'La solicitud fue eliminada correctamente.')
        return redirect('dashboard:panel')

    return render(request, 'dashboard/confirmar_eliminar.html', {'consulta': consulta})
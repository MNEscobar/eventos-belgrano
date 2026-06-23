import json
import requests
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConsultaForm
from django.core.mail import send_mail
from django.conf import settings

def inicio(request):
    """Vista principal - Página de Inicio."""
    context = {
        'titulo': 'Eventos Belgrano',
        'subtitulo': 'Donde los sueños se convierten en recuerdos eternos',
        'pagina_activa': 'inicio',
    }
    return render(request, 'eventos/inicio.html', context)

def servicios(request):
    """Vista de Servicios ofrecidos."""
    servicios_lista = [
        {
            'icono': '💍',
            'titulo': 'Bodas & Casamientos',
            'descripcion': (
                'Creamos el día más especial de su vida con una atención al detalle '
                'incomparable. Desde la ambientación hasta la gastronomía, todo está '
                'pensado para que su historia de amor brille con luz propia.'
            ),
        },
        {
            'icono': '🥂',
            'titulo': 'Eventos Sociales',
            'descripcion': (
                'Cumpleaños de 15, aniversarios, bautismos y celebraciones familiares. '
                'Transformamos cada momento especial en una experiencia memorable '
                'que sus invitados recordarán para siempre.'
            ),
        },
        {
            'icono': '🌿',
            'titulo': 'Ambientación & Decoración',
            'descripcion': (
                'Nuestro equipo de diseño crea atmósferas únicas con flores naturales, '
                'telas premium, iluminación artística y cada detalle cuidadosamente '
                'seleccionado para reflejar su personalidad.'
            ),
        },
        {
            'icono': '🍽️',
            'titulo': 'Gastronomía de Autor',
            'descripcion': (
                'Una propuesta culinaria de excelencia con menús personalizados, '
                'cócteles de bienvenida, banquete completo y servicio de mozos '
                'especializados en eventos de alta gama.'
            ),
        },
        {
            'icono': '📸',
            'titulo': 'Coordinación Integral',
            'descripcion': (
                'Nos encargamos de coordinar cada proveedor: fotografía, video, '
                'música en vivo, DJ, traslados y todo lo necesario para que usted '
                'solo disfrute de su celebración.'
            ),
        },
        {
            'icono': '✨',
            'titulo': 'Consultoría Personalizada',
            'descripcion': (
                'Desde la primera reunión hasta el último vals, acompañamos a cada '
                'familia con asesoramiento exclusivo, presupuestos a medida y '
                'disponibilidad permanente durante todo el proceso.'
            ),
        },
    ]

    context = {
        'titulo': 'Nuestros Servicios',
        'servicios': servicios_lista,
        'pagina_activa': 'servicios',
    }
    return render(request, 'eventos/servicios.html', context)

def galeria(request):
    """Vista de Galería de eventos."""
    # Categorías para filtro visual
    categorias = [
        {'id': 'todos', 'label': 'Todos'},
        {'id': 'bodas', 'label': 'Bodas'},
        {'id': 'sociales', 'label': 'Sociales'},
        {'id': 'decoracion', 'label': 'Decoración'},
    ]

    # Imágenes de la galería con descripciones
    imagenes = [
        {'src': 'boda_salon_1.jpg', 'alt': 'Salón principal decorado para boda', 'categoria': 'bodas', 'titulo': 'Boda Martínez & López'},
        {'src': 'boda_mesa_2.jpg', 'alt': 'Mesa principal floral', 'categoria': 'decoracion', 'titulo': 'Mesa de honor con flores blancas'},
        {'src': 'boda_jardin_3.jpg', 'alt': 'Ceremonia en jardín', 'categoria': 'bodas', 'titulo': 'Ceremonia al aire libre'},
        {'src': 'social_quinces_4.jpg', 'alt': 'Fiesta de 15 años', 'categoria': 'sociales', 'titulo': 'Quinceañera Valentina'},
        {'src': 'deco_flores_5.jpg', 'alt': 'Arreglo floral central', 'categoria': 'decoracion', 'titulo': 'Centros de mesa florales'},
        {'src': 'boda_noche_6.jpg', 'alt': 'Salón iluminado de noche', 'categoria': 'bodas', 'titulo': 'Boda Rodríguez & García'},
        {'src': 'social_aniversario_7.jpg', 'alt': 'Aniversario de bodas de oro', 'categoria': 'sociales', 'titulo': 'Bodas de Oro - Familia Pérez'},
        {'src': 'deco_mesa_8.jpg', 'alt': 'Decoración de mesas', 'categoria': 'decoracion', 'titulo': 'Ambientación minimalista dorada'},
        {'src': 'boda_entrada_9.jpg', 'alt': 'Entrada del salón decorada', 'categoria': 'bodas', 'titulo': 'Boda García & Fernández'},
    ]

    context = {
        'titulo': 'Galería de Eventos',
        'imagenes': imagenes,
        'categorias': categorias,
        'pagina_activa': 'galeria',
    }
    return render(request, 'eventos/galeria.html', context)

def contacto(request):
    """Vista de Contacto con formulario de consultas y reservas."""
    
    # ── 1. CONSUMO DE API EXTERNA (CLIMA EN BELGRANO) ──
    clima = None
    try:
        respuesta = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': -34.5631,
                'longitude': -58.4570,
                'current': 'temperature_2m',
                'timezone': 'America/Argentina/Buenos_Aires',
            },
            timeout=5,
        )
        if respuesta.status_code == 200:
            datos = respuesta.json()
            clima = {
                'temperatura': datos['current']['temperature_2m'],
            }
    except requests.RequestException:
        clima = None  # Si la API externa falla, el sitio sigue funcionando igual

    # ── 2. LÓGICA DEL FORMULARIO ──
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            mensaje_analizar = consulta.mensaje.lower()

            # Clasificación automática
            if any(palabra in mensaje_analizar for palabra in ['precio', 'presupuesto', 'cotización', 'cotizacion', 'costo', 'pagar', 'tarifa', 'reserva']):
                consulta.categoria = 'Comercial'
            elif any(palabra in mensaje_analizar for palabra in ['falla', 'error', 'problema', 'sistema', 'web', 'tecnico', 'técnico', 'bug']):
                consulta.categoria = 'Técnica'
            elif any(palabra in mensaje_analizar for palabra in ['trabajo', 'cv', 'empleo', 'vacante', 'postular', 'rrhh', 'currículum']):
                consulta.categoria = 'RRHH'
            else:
                consulta.categoria = 'General'

            # Guardamos en la base de datos PostgreSQL
            consulta.save()

            # ── 3. ENVÍO DE CORREO AUTOMÁTICO AL USUARIO ──
            asunto = f"[{consulta.get_categoria_display()}] Confirmación de consulta recibida"
            cuerpo = (
                f"Hola {consulta.nombre},\n\n"
                f"Recibimos tu consulta con los siguientes datos:\n\n"
                f"Tipo de evento: {consulta.get_tipo_evento_display()}\n"
                f"Fecha tentativa: {consulta.fecha_evento}\n"
                f"Cantidad de invitados: {consulta.cantidad_invitados}\n"
                f"Mensaje: {consulta.mensaje}\n\n"
                f"Nos pondremos en contacto a la brevedad.\n"
                f"— Eventos Belgrano"
            )
            try:
                send_mail(
                    subject=asunto,
                    message=cuerpo,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[consulta.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error al enviar el correo: {e}")

            # Emitimos el mensaje de éxito y redireccionamos
            messages.success(request, '¡Gracias por su consulta! Nos pondremos en contacto con usted a la brevedad.')
            return redirect('contacto')
        else:
            messages.error(request, 'Por favor, revise los datos ingresados e intente nuevamente.')
    else:
        form = ConsultaForm()
        
    context = {
        'titulo': 'Contacto & Reservas',
        'form': form,
        'pagina_activa': 'contacto',
        'clima': clima, 
    }
    return render(request, 'eventos/contacto.html', context)
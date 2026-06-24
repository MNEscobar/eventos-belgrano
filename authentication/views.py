from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from .models import UsuarioPermitido
from .forms import RegistroForm, ValidacionCodigoForm

def registro(request):
    """Paso 1: nombre, apellido, email y contraseña."""
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            password = form.cleaned_data['password']

            usuario_permitido = UsuarioPermitido.objects.filter(email=email).first()

            # ── Correo NO autorizado ──
            if usuario_permitido is None:
                messages.error(request, 'Acceso restringido. No está autorizado a utilizar este sistema.')
                return render(request, 'authentication/registro.html', {'form': form})

            # ── Ya validado antes ──
            if usuario_permitido.is_registered:
                messages.warning(request, 'Esta cuenta ya fue validada. Por favor, inicie sesión.')
                return redirect('authentication:login')

            # ── Correo autorizado: creamos el usuario INACTIVO hasta validar ──
            user, _ = User.objects.get_or_create(username=email, defaults={'email': email})
            user.first_name = nombre
            user.last_name = apellido
            user.set_password(password)
            user.is_active = False
            user.save()

            enlace_validacion = request.build_absolute_uri(f"/auth/validar/?email={email}")
            try:
                send_mail(
                    subject='Validación de cuenta — Eventos Belgrano',
                    message=(
                        f"Hola {nombre},\n\n"
                        f"Tu código de validación es: {usuario_permitido.codigo_validacion}\n\n"
                        f"Ingresá al siguiente enlace para validar tu cuenta:\n{enlace_validacion}\n\n"
                        f"— Eventos Belgrano"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error al enviar el correo de validación: {e}")

            messages.success(request, 'Le llegará un correo para validar su cuenta.')
            return render(request, 'authentication/registro.html', {'form': RegistroForm()})
    else:
        form = RegistroForm()

    return render(request, 'authentication/registro.html', {'form': form})

def validar_registro(request):
    """Paso 2: el usuario ingresa el código recibido por correo."""
    email_inicial = request.GET.get('email', '')

    if request.method == 'POST':
        form = ValidacionCodigoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            codigo = form.cleaned_data['codigo']

            try:
                usuario_permitido = UsuarioPermitido.objects.get(email=email, codigo_validacion=codigo)
            except UsuarioPermitido.DoesNotExist:
                messages.error(request, 'El código ingresado no es correcto.')
                return render(request, 'authentication/validar.html', {'form': form})

            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                messages.error(request, 'Primero debe completar el registro.')
                return redirect('authentication:registro')

            user.is_active = True
            user.save()
            usuario_permitido.is_registered = True
            usuario_permitido.save()

            messages.success(request, '¡Cuenta validada con éxito! Ya puede iniciar sesión.')
            return redirect('authentication:login')
    else:
        form = ValidacionCodigoForm(initial={'email': email_inicial})

    return render(request, 'authentication/validar.html', {'form': form})

def iniciar_sesion(request):
    """Sin cambios respecto a lo que ya tenías."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:panel')
        else:
            messages.error(request, 'Credenciales inválidas. Intente nuevamente.')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Ha cerrado sesión exitosamente.')
    return redirect('inicio')
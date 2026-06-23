from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import UsuarioPermitido
from .forms import ValidacionRegistroForm

def validar_registro(request):
    """Vista para validar el código secreto y crear el usuario nativo."""
    if request.method == 'POST':
        form = ValidacionRegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            codigo = form.cleaned_data['codigo']
            password = form.cleaned_data['password']

            try:
                # 1. Buscamos si el usuario está en la lista blanca
                usuario_permitido = UsuarioPermitido.objects.get(email=email, codigo_validacion=codigo)

                # 2. Verificamos que no se haya registrado antes
                if usuario_permitido.is_registered:
                    messages.warning(request, 'Este usuario ya validó su cuenta. Por favor, inicie sesión.')
                    return redirect('authentication:login')

                # 3. Creamos el usuario nativo de Django
                # Usamos el email como username porque es único
                user = User.objects.create_user(username=email, email=email, password=password)
                user.first_name = usuario_permitido.nombre
                user.save()

                # 4. Inutilizamos el código secreto
                usuario_permitido.is_registered = True
                usuario_permitido.save()

                messages.success(request, '¡Cuenta activada con éxito! Ya puede iniciar sesión.')
                return redirect('authentication:login')

            except UsuarioPermitido.DoesNotExist:
                messages.error(request, 'El correo o el código son incorrectos, o no tiene acceso al sistema.')
    else:
        form = ValidacionRegistroForm()

    return render(request, 'authentication/validar.html', {'form': form})


def iniciar_sesion(request):
    """Vista para loguearse utilizando el sistema nativo de Django."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:panel') # Redirige directo al panel protegido
        else:
            messages.error(request, 'Credenciales inválidas. Intente nuevamente.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'authentication/login.html', {'form': form})


def cerrar_sesion(request):
    """Vista para destruir la sesión segura."""
    logout(request)
    messages.info(request, 'Ha cerrado sesión exitosamente.')
    return redirect('inicio') # Redirigimos a la landing page pública
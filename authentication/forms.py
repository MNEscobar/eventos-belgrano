from django import forms
from django.contrib.auth.password_validation import validate_password

class RegistroForm(forms.Form):
    """Paso 1: datos para el registro."""
    nombre = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ana'})
    )
    apellido = forms.CharField(
        label='Apellido',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Villegas'})
    )
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'su@email.com'})
    )
    password = forms.CharField(
        label='Contraseña Segura',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Reutiliza los AUTH_PASSWORD_VALIDATORS ya definidos en settings.py
        validate_password(password)
        return password

class ValidacionCodigoForm(forms.Form):
    """Paso 2: solo pide el código; el email viaja oculto desde el enlace del mail."""
    email = forms.EmailField(widget=forms.HiddenInput())
    codigo = forms.CharField(
        label='Código de Validación',
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A1B2C3'})
    )
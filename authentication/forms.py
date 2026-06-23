from django import forms

class ValidacionRegistroForm(forms.Form):
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'su@email.com'})
    )
    codigo = forms.CharField(
        label='Código de Validación',
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A1B2C3'})
    )
    password = forms.CharField(
        label='Cree una Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
    )
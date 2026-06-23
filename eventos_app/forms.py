from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Consulta


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = [
            'nombre', 'email', 'telefono',
            'tipo_evento', 'fecha_evento',
            'cantidad_invitados', 'mensaje'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control eb-input',
                'placeholder': 'Su nombre completo',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control eb-input',
                'placeholder': 'su@email.com',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control eb-input',
                'placeholder': '+54 11 XXXX-XXXX',
            }),
            'tipo_evento': forms.Select(attrs={
                'class': 'form-select eb-input',
            }),
            'fecha_evento': forms.DateInput(attrs={
                'class': 'form-control eb-input',
                'type': 'date',
            }),
            'cantidad_invitados': forms.NumberInput(attrs={
                'class': 'form-control eb-input',
                'placeholder': 'Ej: 150',
                'min': '1',
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control eb-input',
                'rows': 5,
                'placeholder': 'Cuéntenos sobre el evento de sus sueños...',
            }),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono de Contacto',
            'tipo_evento': 'Tipo de Evento',
            'fecha_evento': 'Fecha Tentativa',
            'cantidad_invitados': 'Cantidad de Invitados',
            'mensaje': 'Su Mensaje',
        }

        # ── VALIDACIÓN DE BACKEND PARA LA FECHA ───────────────────
        def clean_fecha_evento(self):
            fecha_evento = self.cleaned_data.get('fecha_evento')
            hoy = timezone.now().date() # Obtenemos solo la fecha de hoy (sin hora)
            
            if fecha_evento and fecha_evento < hoy:
                raise ValidationError(
                    "La fecha tentativa no puede ser anterior a la fecha actual."
                    )
            # Siempre se debe retornar el campo limpio
            return fecha_evento
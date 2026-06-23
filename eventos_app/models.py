from django.db import models


class Consulta(models.Model):
    TIPO_EVENTO_CHOICES = [
        ('casamiento', 'Casamiento'),
        ('cumpleanos', 'Cumpleaños'),
        ('corporativo', 'Evento Corporativo'),
        ('bautismo', 'Bautismo'),
        ('otro', 'Otro'),
    ]

    CATEGORIA_CHOICES = [
        ('Comercial', 'Consulta Comercial'),
        ('Técnica', 'Consulta Técnica'),
        ('RRHH', 'Consulta de RRHH'),
        ('General', 'Consulta General'),
        ('Pendiente', 'Pendiente de Clasificación'), # Valor por defecto seguro
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre completo')
    email = models.EmailField(verbose_name='Correo electrónico')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    tipo_evento = models.CharField(
        max_length=20,
        choices=TIPO_EVENTO_CHOICES,
        default='casamiento',
        verbose_name='Tipo de evento'
    )
    fecha_evento = models.DateField(verbose_name='Fecha tentativa del evento')
    cantidad_invitados = models.PositiveIntegerField(
        verbose_name='Cantidad de invitados aproximada'
    )
    mensaje = models.TextField(
        verbose_name='Mensaje o consulta',
        help_text='Cuéntenos sobre su evento soñado...'
    )
    fecha_consulta = models.DateTimeField(auto_now_add=True)

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default='Pendiente',
        verbose_name='Categoría de la consulta'
    )

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-fecha_consulta']

    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_evento_display()} | Categoría: {self.get_categoria_display()}"

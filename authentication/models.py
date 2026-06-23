from django.db import models

class UsuarioPermitido(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    # unique=True garantiza que no haya dos registros para el mismo cliente
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    # Usaremos una cadena alfanumérica de 6 caracteres para el código
    codigo_validacion = models.CharField(max_length=6, unique=True, verbose_name="Código de Validación")
    # Bandera para saber si el cliente ya completó el registro
    is_registered = models.BooleanField(default=False, verbose_name="¿Usuario Registrado?")

    class Meta:
        verbose_name = "Usuario Permitido"
        verbose_name_plural = "Usuarios Permitidos"

    def __str__(self):
        return f"{self.nombre} - {self.email}"

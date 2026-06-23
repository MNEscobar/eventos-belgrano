from django.db import migrations

def cargar_profesora(apps, schema_editor):
    # Obtenemos el modelo histórico para no romper la migración
    UsuarioPermitido = apps.get_model('authentication', 'UsuarioPermitido')
    
    # Creamos el registro exigido por la consigna
    UsuarioPermitido.objects.create(
        nombre='Analía Villegas',
        email='annavillegas@live.com.ar',
        codigo_validacion='WEB226', # Este será el código secreto
        is_registered=False
    )

class Migration(migrations.Migration):

    dependencies = [
        # Depende de la migración inicial donde se creó la tabla
        ('authentication', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(cargar_profesora),
    ]
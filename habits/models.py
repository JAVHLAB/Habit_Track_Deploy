from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

class Habito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='habitos')
    nombre = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, blank=True)  # Puede ser un emoji o un símbolo
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    dias_semana = models.CharField(max_length=50)  # dias_semana = models.CharField(max_length=50)  # Podrías usar un campo JSON para más flexibilidad
    rango_tiempo_inicio = models.TimeField()
    rango_tiempo_fin = models.TimeField()
    recordatorio = models.BooleanField(default=False)
    recordatorio_hora = models.TimeField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=50)
    fecha_envio = models.DateTimeField()
    mensaje = models.TextField()

class Nota(models.Model):
    habito = models.ForeignKey(Habito, on_delete=models.CASCADE, related_name='notas')
    contenido = models.TextField()
    fecha = models.DateField()

class Ejecucion(models.Model):
    habito = models.ForeignKey(Habito, on_delete=models.CASCADE, related_name='ejecuciones')
    fecha = models.DateField()
    completado = models.BooleanField(default=False)

class Estadisticas(models.Model):
    habito = models.ForeignKey(Habito, on_delete=models.CASCADE, related_name='estadisticas')
    dias_transcurridos = models.IntegerField()
    dias_completados = models.IntegerField()
    efectividad = models.FloatField()

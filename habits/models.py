from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re

class Usuario(AbstractUser):
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)  # Esto asegura que el correo sea único

class Habito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='habitos')
    nombre = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, blank=True)  # Puede ser un emoji o un símbolo
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    rango_tiempo_inicio = models.TimeField(blank=True, null=True)
    rango_tiempo_fin = models.TimeField(blank=True, null=True)
    recordatorio = models.BooleanField(default=False)
    hora_recordatorio = models.TimeField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=50)
    fecha_envio = models.DateTimeField()
    mensaje = models.TextField()
    es_random = models.BooleanField(default=False)

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

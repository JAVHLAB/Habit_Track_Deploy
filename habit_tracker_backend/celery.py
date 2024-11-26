import random
from datetime import datetime
from celery import shared_task
from .models import Usuario, Notificacion
from expo_push import send_expo_notification

@shared_task
def enviar_notificaciones_random():
    usuarios = Usuario.objects.filter(token_push__isnull=False)  # Solo usuarios con token push
    mensajes_random = [
        "¡No olvides revisar tus hábitos hoy!",
        "¡Mantente constante, estás haciendo un gran trabajo!",
        "¡Hoy es un buen día para cumplir tus metas!",
        "¡Sigue adelante! Tus hábitos te acercan a tus objetivos.",
        "¡Recuerda registrar tus logros de hoy!"
    ]

    for usuario in usuarios:
        mensaje = random.choice(mensajes_random)  # Seleccionar un mensaje aleatorio
        send_expo_notification(usuario.token_push, mensaje)

        # Registrar la notificación en la base de datos
        Notificacion.objects.create(
            usuario=usuario,
            tipo="random",
            fecha_envio=datetime.now(),
            mensaje=mensaje,
            es_random=True
        )
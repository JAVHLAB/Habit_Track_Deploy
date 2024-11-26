from celery import shared_task
from datetime import datetime
from .models import Habito, Notificacion
from expo_push import send_expo_notification

@shared_task
def enviar_notificaciones_programadas():
    ahora = datetime.now()
    habitos = Habito.objects.filter(hora_recordatorio__isnull=False)

    for habito in habitos:
        usuario = habito.usuario
        hora_actual = ahora.time()
        if hora_actual >= habito.hora_recordatorio:
            mensaje = f"¡Hora de cumplir con tu hábito: {habito.nombre}!"
            send_expo_notification(usuario.token_push, mensaje)

            # Registrar notificación en la base de datos
            Notificacion.objects.create(
                usuario=usuario,
                tipo="recordatorio",
                fecha_envio=ahora,
                mensaje=mensaje,
                es_random=False
            )
from rest_framework import viewsets
from .models import Usuario, Habito, Notificacion, Nota, Ejecucion, Estadisticas
from .serializers import UsuarioSerializer, HabitoSerializer, NotificacionSerializer, NotaSerializer, EjecucionSerializer, EstadisticasSerializer

import random
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from datetime import date
from django.db.models import Min
from datetime import timedelta



class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class HabitoViewSet(viewsets.ModelViewSet):
    queryset = Habito.objects.all()
    serializer_class = HabitoSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        # Si recordatorio es True y hora_recordatorio no se establece
        if data.get("recordatorio") and not data.get("hora_recordatorio"):
            rango_tiempo_inicio = data.get("rango_tiempo_inicio")
            if rango_tiempo_inicio:
                # Restar 10 minutos al rango_tiempo_inicio
                from datetime import datetime
                rango_tiempo_inicio_dt = datetime.strptime(rango_tiempo_inicio, "%H:%M")
                hora_recordatorio_dt = rango_tiempo_inicio_dt - timedelta(minutes=10)
                data["hora_recordatorio"] = hora_recordatorio_dt.strftime("%H:%M")

        # Serializar y validar los datos
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Guardar el objeto
        self.perform_create(serializer)

        # Retornar respuesta
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    
    def get_queryset(self):
            user_id = self.request.query_params.get('userId')  
            if user_id:
                return Habito.objects.filter(usuario=user_id)  
            return super().get_queryset()
    

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

class EjecucionViewSet(viewsets.ModelViewSet):
    queryset = Ejecucion.objects.all()
    serializer_class = EjecucionSerializer

    @action(detail=False, methods=['post'])
    def marcar_habito(self, request):
        """
        Marca o desmarca un hábito. Si el hábito ya tiene un registro para el día,
        actualiza el campo 'completado'. Si no existe, crea uno nuevo.
        """
        habit_id = request.data.get('habito')
        fecha = request.data.get('fecha')

        # Validar si los datos son correctos
        if not habit_id or not fecha:
            return Response({"error": "Debe proporcionar un hábito y una fecha."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            habit = Habito.objects.get(id=habit_id)  # Verificamos que el hábito exista
        except Habito.DoesNotExist:
            return Response({"error": "El hábito no existe."}, status=status.HTTP_404_NOT_FOUND)

        
        # Verificamos si ya existe una ejecución para ese hábito y fecha
        ejecucion, created = Ejecucion.objects.get_or_create(habito=habit, fecha=fecha)

        self.actualizar_estadisticas(habit)

        # Serializamos la respuesta
        serializer = self.get_serializer(ejecucion)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def actualizar_estadisticas(self, habit):
        """
        Calcula y actualiza las estadísticas del hábito.
        """
        # Obtener todas las ejecuciones del hábito
        ejecuciones = Ejecucion.objects.filter(habito=habit, completado=False).order_by('fecha')

        if ejecuciones.exists():
            # Calcular estadísticas
            fecha_mas_antigua = ejecuciones.aggregate(Min('fecha'))['fecha__min']
            dias_transcurridos = (date.today() - fecha_mas_antigua).days + 1
            dias_completados = ejecuciones.count()
            efectividad = dias_completados / dias_transcurridos if dias_transcurridos > 0 else 0

            # Actualizar o crear estadísticas
            Estadisticas.objects.update_or_create(
                habito=habit,
                defaults={
                    'dias_transcurridos': dias_transcurridos,
                    'dias_completados': dias_completados,
                    'efectividad': efectividad,
                }
            )

    @action(detail=False, methods=['get'])
    def filtrar_por_usuario_y_fecha(self, request):
            """
            Filtra las ejecuciones de un usuario por fecha.
            """
            user_id = request.query_params.get('userId')
            fecha = request.query_params.get('fecha')

            if not user_id or not fecha:
                return Response({"error": "userId y fecha son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                ejecuciones = Ejecucion.objects.filter(
                    habito__usuario_id=user_id,  # Asumiendo que "usuario" está relacionado con el "habito"
                    fecha=fecha
                )
            except Ejecucion.DoesNotExist:
                return Response({"error": "No se encontraron ejecuciones."}, status=status.HTTP_404_NOT_FOUND)

            # Serializar los resultados
            serializer = EjecucionSerializer(ejecuciones, many=True)
            return Response(serializer.data)    


class EstadisticasViewSet(viewsets.ModelViewSet):
    queryset = Estadisticas.objects.all()
    serializer_class = EstadisticasSerializer

    @action(detail=False, methods=['get'])
    def filtrar_por_usuario_y_fecha(self, request):
        """
        Filtra las ejecuciones y las estadísticas de un usuario por fecha.
        """
        user_id = request.query_params.get('userId')
        fecha = request.query_params.get('fecha')

        if not user_id or not fecha:
            return Response({"error": "userId y fecha son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar las ejecuciones del usuario y la fecha
        ejecuciones = Ejecucion.objects.filter(
            habito__usuario_id=user_id,  # Asumiendo que "usuario" está relacionado con el "habito"
            fecha=fecha
        )

        # Filtrar las estadísticas del usuario para los hábitos de ese día
        estadisticas = Estadisticas.objects.filter(
            habito__usuario_id=user_id,  # Relacionar con el usuario
            habito__ejecuciones__fecha=fecha  # Asegurar que el hábito tiene ejecuciones en esa fecha
        )

        if not ejecuciones and not estadisticas:
            return Response({
                "ejecuciones": [],
                "estadisticas": []
            })


        # Serializar las ejecuciones
        ejecuciones_serializer = EjecucionSerializer(ejecuciones, many=True)

        # Serializar las estadísticas
        estadisticas_serializer = EstadisticasSerializer(estadisticas, many=True)

        # Devolver los resultados
        return Response({
            "ejecuciones": ejecuciones_serializer.data,
            "estadisticas": estadisticas_serializer.data
        })


# Correo de verificación
class SendVerificationCodeView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({'message': 'El email es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generar un código numérico de 5 dígitos
        code = random.randint(10000, 99999)

        # Enviar el correo
        subject = 'Código de Verificación'
        message = f'Tu código de verificación es: {code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            # Incluir el código en la respuesta
            return Response({'message': 'Código enviado exitosamente.', 'code': code}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Error al enviar el correo.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(Usuario, email=request.data['email'])

    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsuarioSerializer(instance=user)

    return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def checkdata(request):
    username = request.data.get('username')
    email = request.data.get('email')

    if Usuario.objects.filter(username=username).exists():
        return Response({'error': 'El nombre de usuario ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Usuario.objects.filter(email=email).exists():
        return Response({'error': 'El correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'message': 'Los datos son válidos. Puedes proceder con el registro.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def resetpassword(request):
    user = get_object_or_404(Usuario, email=request.data['email'])

    user.set_password(request.data['password'])
    user.save()
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsuarioSerializer(instance=user)

    return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = Usuario.objects.get(email=serializer.data['email'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):

    print(request.user)

    return Response("You are login with {}".format(request.user.username), status=status.HTTP_200_OK)
"""

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user  

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "foto_perfil": request.build_absolute_uri(user.foto_perfil.url) if user.foto_perfil else None
    }, status=status.HTTP_200_OK)
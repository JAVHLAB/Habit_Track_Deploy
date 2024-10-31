from rest_framework import viewsets
from .models import Usuario, Habito, Notificacion, Nota, Ejecucion, Estadisticas
from .serializers import UsuarioSerializer, HabitoSerializer, NotificacionSerializer, NotaSerializer, EjecucionSerializer, EstadisticasSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class HabitoViewSet(viewsets.ModelViewSet):
    queryset = Habito.objects.all()
    serializer_class = HabitoSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

class EjecucionViewSet(viewsets.ModelViewSet):
    queryset = Ejecucion.objects.all()
    serializer_class = EjecucionSerializer

class EstadisticasViewSet(viewsets.ModelViewSet):
    queryset = Estadisticas.objects.all()
    serializer_class = EstadisticasSerializer

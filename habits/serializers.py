from rest_framework import serializers
from .models import Usuario, Habito, Notificacion, Nota, Ejecucion, Estadisticas

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'foto_perfil', 'fecha_registro']

class HabitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habito
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'

class EjecucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejecucion
        fields = '__all__'

class EstadisticasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estadisticas
        fields = '__all__'

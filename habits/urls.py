from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, HabitoViewSet, NotificacionViewSet, NotaViewSet, EjecucionViewSet, EstadisticasViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'habitos', HabitoViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'notas', NotaViewSet)
router.register(r'ejecuciones', EjecucionViewSet)
router.register(r'estadisticas', EstadisticasViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

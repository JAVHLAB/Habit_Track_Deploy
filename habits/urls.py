from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, HabitoViewSet, NotificacionViewSet, NotaViewSet, EjecucionViewSet, EstadisticasViewSet, SendVerificationCodeView
from . import views

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'habitos', HabitoViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'notas', NotaViewSet)
router.register(r'ejecuciones', EjecucionViewSet)
router.register(r'estadisticas', EstadisticasViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send-code/', SendVerificationCodeView.as_view(), name='send-code'),
    re_path('login/', views.login),
    re_path('register/', views.register),
    re_path('profile/', views.profile),
    re_path('resetpassword/', views.resetpassword),
    re_path('checkdata/', views.checkdata),
]


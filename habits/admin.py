from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Habito)
admin.site.register(Notificacion)
admin.site.register(Nota)
admin.site.register(Ejecucion)
admin.site.register(Estadisticas)
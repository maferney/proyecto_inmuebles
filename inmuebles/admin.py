from django.contrib import admin
from .models import Usuario, Inmueble, SolicitudArriendo, Region, Comuna
from django.utils import timezone
from django.core.exceptions import PermissionDenied

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'tipo_usuario', 'rut', 'correo', 'telefono')  
    search_fields = ('username', 'rut', 'correo')  
    list_filter = ('tipo_usuario',)
    readonly_fields = ('date_joined', 'last_login')  # Campos de solo lectura
    def save_model(self, request, obj, form, change):
        if not change:
            obj.date_joined = timezone.now()
        obj.save()
    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'precio', 'comuna', 'arrendador')  
    search_fields = ('nombre', 'direccion', 'comuna__nombre')  
    list_filter = ('tipo_inmueble', 'comuna')  
    readonly_fields = ('fecha_creacion', 'ultima_modificacion')  

    def save_model(self, request, obj, form, change):
        # Validar si el usuario que realiza la acción existe
        if not Usuario.objects.filter(id=request.user.id).exists():
            raise PermissionDenied("El usuario autenticado no es válido.")
        
        # Actualizar las fechas según si el objeto está siendo modificado o creado
        if change:
            obj.ultima_modificacion = timezone.now()
        else:
            obj.fecha_creacion = timezone.now()
        
        obj.save()

@admin.register(SolicitudArriendo)
class SolicitudArriendoAdmin(admin.ModelAdmin):
    list_display = ('id', 'inmueble', 'arrendatario', 'fecha_solicitud', 'estado')  
    search_fields = ('inmueble__nombre', 'arrendatario__username')  
    list_filter = ('estado', 'fecha_solicitud')  
    readonly_fields = ('fecha_solicitud',)  

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  
    search_fields = ('nombre',)  
    list_filter = ('nombre',)  

@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'region')  
    search_fields = ('nombre', 'region__nombre')  
    list_filter = ('region',)  

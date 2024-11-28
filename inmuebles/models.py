from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import uuid

# Create your models here.

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('arrendatario', 'Arrendatario'),
        ('arrendador', 'Arrendador'),
    ]
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_groups',  # Nombre único para evitar conflictos
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions',  # Nombre único para evitar conflictos
        blank=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.tipo_usuario}"


class Inmueble(models.Model):
    TIPO_INMUEBLE_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela', 'Parcela'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    m2_construidos = models.FloatField()
    m2_terreno = models.FloatField()
    estacionamientos = models.IntegerField()
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    direccion = models.CharField(max_length=255)
    comuna = models.ForeignKey('Comuna', on_delete=models.CASCADE)
    tipo_inmueble = models.CharField(max_length=20, choices=TIPO_INMUEBLE_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    arrendador = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name="inmuebles")
    imagen = models.ImageField(upload_to='inmuebles/', blank=True, null=True)  # Campo para imágenes
    fecha_creacion = models.DateTimeField(default=now, editable=False)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class SolicitudArriendo(models.Model):
    arrendatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="solicitudes")
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name="solicitudes")
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="pendiente")

    def _str_(self):
        return f"Solicitud {self.id} para {self.inmueble.nombre}"
    

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.region.nombre})"

class ContactForm(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_name = models.CharField(max_length=64)
    customer_email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.customer_name
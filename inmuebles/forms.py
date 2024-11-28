from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario, ContactForm, Inmueble, Comuna, Region 
import re


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nombre"
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Apellido"
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Correo electrónico"
    )
    tipo_usuario = forms.ChoiceField(
        choices=Usuario.TIPO_USUARIO_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de usuario"
    )
    rut = forms.CharField(
        max_length=12, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="RUT"
    )
    direccion = forms.CharField(
        max_length=200, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Dirección"
    )
    telefono = forms.CharField(
        max_length=15, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Teléfono"
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'tipo_usuario', 'rut', 'direccion', 'telefono']
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña'
        }


def clean_rut(self):
    """Valida que el RUT sea correcto."""
    rut = self.cleaned_data.get('rut')

    # Eliminar puntos y guiones
    rut = rut.replace(".", "").replace("-", "").upper()

    # Verificar formato
    if not re.match(r'^\d{7,8}[0-9K]$', rut):
        raise forms.ValidationError("El RUT ingresado no tiene un formato válido.")

    # Separar número base y dígito verificador
    rut_base = rut[:-1]
    digito_verificador = rut[-1]

    # Validar el dígito verificador
    if not self.validar_dv(rut_base, digito_verificador):
        raise forms.ValidationError("El RUT ingresado no es válido.")

    return rut

def validar_dv(self, rut_base, digito_verificador):
    """Verifica el dígito verificador del RUT."""
    suma = 0
    multiplicador = 2

    for digito in reversed(rut_base):
        suma += int(digito) * multiplicador
        multiplicador = 9 if multiplicador == 7 else multiplicador + 1

    resto = suma % 11
    dv_esperado = 11 - resto
    if dv_esperado == 11:
        dv_esperado = "0"
    elif dv_esperado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_esperado)

    return digito_verificador == dv_esperado

class ActualizarUsuarioForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Nombre de usuario")
    first_name = forms.CharField(max_length=30, required=False, label="Nombre")
    last_name = forms.CharField(max_length=30, required=False, label="Apellido")
    email = forms.EmailField(required=False, label="Correo electrónico")
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Deja en blanco para no cambiar la contraseña'}),
        label="Contraseña nueva (opcional)",
    )

    class Meta:
        model = Usuario
        fields = ['rut', 'direccion', 'telefono', 'username']  # Incluye todos los campos relevantes

    def save(self, commit=True):
        user = super().save(commit=False)

        # Actualizar campos adicionales del modelo Usuario
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])  # Cambiar contraseña si se proporciona

        if commit:
            user.save()
        return user

class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['customer_name', 'customer_email', 'message']
        labels = {
            'customer_name': 'Nombre',
            'customer_email': 'Email',
            'message': 'Mensaje',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'placeholder': 'Tu nombre',
                'class': 'form-control rounded-pill border-primary shadow-sm',
                'style': 'max-width: 500px;'
            }),
            'customer_email': forms.EmailInput(attrs={
                'placeholder': 'Correo electrónico',
                'class': 'form-control rounded-pill border-primary shadow-sm',
                'style': 'max-width: 500px;'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tu mensaje',
                'rows': 4,
                'class': 'form-control border-primary shadow-sm',
                'style': 'max-width: 500px;'
            }),
        }

from django import forms
from .models import Inmueble, Comuna, Region

class InmuebleForm(forms.ModelForm):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label="Selecciona una región",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Región"
    )

    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        empty_label="Selecciona una comuna",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Comuna"
    )

    class Meta:
        model = Inmueble
        fields = [
            'nombre', 'descripcion', 'm2_construidos', 'm2_terreno',
            'estacionamientos', 'habitaciones', 'banos', 'direccion',
            'region', 'comuna', 'tipo_inmueble', 'precio', 'imagen'
        ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'm2_construidos': 'Metros cuadrados construidos',
            'm2_terreno': 'Metros cuadrados de terreno',
            'estacionamientos': 'Número de estacionamientos',
            'habitaciones': 'Número de habitaciones',
            'banos': 'Número de baños',
            'direccion': 'Dirección',
            'comuna': 'Comuna',
            'region': 'Región',
            'tipo_inmueble': 'Tipo de inmueble',
            'precio': 'Precio',
            'imagen': 'Imagen del inmueble',  # Etiqueta para el campo de imagen
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),  # Widget para región
            'comuna': forms.Select(attrs={'class': 'form-control'}),  # Widget para comuna
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),  # Widget para subir imágenes
        }

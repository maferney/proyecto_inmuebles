from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from inmuebles.forms import ActualizarUsuarioForm, ContactFormForm, CustomUserCreationForm, InmuebleForm
from inmuebles.models import Usuario, Inmueble
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def logout(request):
    return render(request, 'logout.html')

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # No guardar aún en la DB
            tipo_usuario = form.cleaned_data.get('tipo_usuario')
            user.set_password(form.cleaned_data['password1'])  # Asegura que la contraseña esté cifrada
            user.tipo_usuario = tipo_usuario  # Asigna el tipo de usuario
            user.save()  # Guarda el usuario con el tipo de usuario

            login(request, user)  # Inicia sesión automáticamente

            # Redirige según el tipo de usuario
            if tipo_usuario == 'arrendatario':
                return redirect('arrendatario')  # Redirige al perfil de arrendatario
            elif tipo_usuario == 'arrendador':
                return redirect('arrendador')  # Redirige al perfil de arrendador
            else:
                return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def actualizar_usuario(request):
    if request.method == 'POST':
        form = ActualizarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()

            # Mantener la sesión activa si cambia la contraseña
            if form.cleaned_data.get('password'):
                update_session_auth_hash(request, user)

            # Mensaje de éxito
            messages.success(request, 'Has actualizado tus datos con éxito')

            # Redirigir al perfil adecuado según el tipo de usuario
            if user.tipo_usuario == 'arrendador':
                return redirect('arrendador')  # URL para el perfil de arrendador
            elif user.tipo_usuario == 'arrendatario':
                return redirect('arrendatario')  # URL para el perfil de arrendatario
            else:
                return redirect('perfil')  # Redirige a algún perfil predeterminado si no es arrendador ni arrendatario
    else:
        form = ActualizarUsuarioForm(instance=request.user)

    return render(request, 'actualizar_usuario.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Su mensaje se ha enviado con éxito.')
            return redirect('contacto')  
    else:
        form = ContactFormForm()
    return render(request, 'contacto.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Obtén el usuario autenticado
            login(request, user)  # Inicia sesión automáticamente

            # Redirige según el tipo de usuario
            if user.tipo_usuario == 'arrendatario':
                return redirect('arrendatario')  # Redirige a la página de arrendatario
            elif user.tipo_usuario == 'arrendador':
                return redirect('arrendador')  # Redirige a la página de arrendador
            else:
                return redirect('home')  # Redirige al home si no es arrendatario ni arrendador
    else:
        form = AuthenticationForm()

    # Pasa el usuario autenticado a la plantilla
    return render(request, 'registration/login.html', {'form': form, 'usuario': request.user})

@login_required
def arrendatario_view(request):
    if request.user.is_authenticated:
        usuario = request.user
        return render(request, 'arrendatario.html', {'usuario': usuario})
    else:
        return redirect('login')
    
@login_required
def arrendador_view(request):
    if request.user.is_authenticated and request.user.tipo_usuario == 'arrendador':
        usuario = request.user
        # Obtener los inmuebles del arrendador (usuario)
        inmuebles = Inmueble.objects.filter(arrendador=usuario)
        return render(request, 'arrendador.html', {'usuario': usuario, 'inmuebles': inmuebles})
    else:
        return redirect('login')

@login_required
def agregar_inmueble(request):
    if request.user.tipo_usuario != 'arrendador':
        return redirect('home')  # Redirige si el usuario no es arrendador

    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES)  # Aquí se debe incluir `request.FILES` para que los archivos se gestionen
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.arrendador = request.user  # Asocia el inmueble con el arrendador actual
            inmueble.save()

            # Agregar el mensaje de éxito
            messages.success(request, 'Inmueble creado con éxito.')

            return redirect('mis_inmuebles')  # Redirige a la página que muestra los inmuebles creados por el usuario
    else:
        form = InmuebleForm()
    return render(request, 'agregar_inmueble.html', {'form': form})

@login_required
def mis_inmuebles(request):
    # Filtrar los inmuebles que pertenecen al usuario actual
    inmuebles = Inmueble.objects.filter(arrendador=request.user)

    return render(request, 'mis_inmuebles.html', {'inmuebles': inmuebles})

@login_required
def editar_inmueble(request, id):
    inmueble = get_object_or_404(Inmueble, id=id)

    # Verificar que el usuario es el arrendador del inmueble
    if request.user != inmueble.arrendador:
        messages.error(request, 'No tienes permiso para editar este inmueble.')
        return redirect('mis_inmuebles')

    if request.method == 'POST':
        form = InmuebleForm(request.POST, request.FILES, instance=inmueble)  # Manejo de archivos
        if form.is_valid():
            form.save()
            messages.success(request, 'Inmueble actualizado con éxito.')
            return redirect('mis_inmuebles')
    else:
        form = InmuebleForm(instance=inmueble)

    return render(request, 'editar_inmueble.html', {'form': form, 'inmueble': inmueble})

@login_required
def eliminar_inmueble(request, id):
    inmueble = get_object_or_404(Inmueble, id=id)
    
    # Verificar si el usuario es el arrendador del inmueble
    if request.user != inmueble.arrendador:
        messages.error(request, 'No tienes permiso para eliminar este inmueble.')
        return redirect('mis_inmuebles')

    # Eliminar el inmueble
    inmueble.delete()
    messages.success(request, 'Inmueble eliminado con éxito.')
    
    return redirect('mis_inmuebles')  # Redirige a la página de los inmuebles

@login_required
def exito(request):
    user = request.user  # Obtener el usuario actual
    if hasattr(user, 'tipo_usuario'):  # Verificar que el atributo tipo_usuario existe
        tipo_usuario = user.tipo_usuario
    else:
        tipo_usuario = None  # O manejar el caso cuando no exista el atributo

    # Pasar la información al template
    return render(request, 'exito.html', {'tipo_usuario': tipo_usuario})

@login_required
def ver_oferta(request):
    # Filtrar inmuebles disponibles para arrendar
    inmuebles = Inmueble.objects.filter(arrendador__tipo_usuario='arrendador')  # Inmuebles creados por arrendadores
    return render(request, 'ver_oferta.html', {'inmuebles': inmuebles})

@login_required
def confirmar_eliminacion_inmueble(request, id):
    # Obtén el inmueble que deseas eliminar
    inmueble = get_object_or_404(Inmueble, id=id)

    # Verifica si el usuario es el arrendador del inmueble
    if request.user != inmueble.arrendador:
        messages.error(request, "No tienes permiso para eliminar este inmueble.")
        return redirect('mis_inmuebles')

    if request.method == 'POST':
        # Si el formulario es enviado, eliminamos el inmueble
        inmueble.delete()
        messages.success(request, 'Inmueble eliminado con éxito.')
        return redirect('mis_inmuebles')  # Redirige al listado de inmuebles

    return render(request, 'confirmar_eliminacion.html', {'inmueble': inmueble})

@login_required
def ver_inmuebles(request):
    # Solo mostramos inmuebles creados por arrendadores (sin necesidad de filtrar por solicitudes de arrendatario)
    inmuebles = Inmueble.objects.all()  # Puedes agregar filtros si es necesario, como solo mostrar inmuebles disponibles

    return render(request, 'ver_inmuebles.html', {'inmuebles': inmuebles})

@login_required
def detalle_inmueble(request, id):
    inmueble = get_object_or_404(Inmueble, id=id)
    return render(request, 'detalle_inmueble.html', {'inmueble': inmueble})
"""
URL configuration for inmobiliaria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import custom_login 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.registro, name='register'),
    path('update_profile/', views.actualizar_usuario, name='update_profile'),
    path('', views.home, name='home'),
    path('contacto/', views.contact, name='contacto'),
    path('exito/', views.exito, name='exito'),
    path('accounts/login/', views.custom_login, name='login'),
    path('arrendatario/', views.arrendatario_view, name='arrendatario'),
    path('arrendador/', views.arrendador_view, name='arrendador'),
    path('inmuebles/nuevo/', views.agregar_inmueble, name='agregar_inmueble'),
    path('mis_inmuebles/', views.mis_inmuebles, name='mis_inmuebles'), 
    path('inmuebles/editar/<int:id>/', views.editar_inmueble, name='editar_inmueble'),
    path('inmuebles/eliminar/<int:id>/', views.eliminar_inmueble, name='eliminar_inmueble'),
    path('inmuebles/eliminar/confirmar/<int:id>/', views.confirmar_eliminacion_inmueble, name='confirmar_eliminacion_inmueble'),
    path('inmuebles/disponibles/', views.ver_inmuebles, name='ver_inmuebles'),
    path('inmuebles/detalle/<int:id>/', views.detalle_inmueble, name='detalle_inmueble'),
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


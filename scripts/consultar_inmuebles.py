import os
import django
import sys

# Añadir el directorio principal de tu proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inmobiliaria.settings')
django.setup()

# Importar el modelo Inmueble
from inmuebles.models import Inmueble

# Función para consultar inmuebles por comuna
def consultar_inmuebles_por_comuna():
    inmuebles_por_comuna = Inmueble.objects.values('comuna').distinct()

    with open('inmuebles_por_comuna.txt', 'w') as archivo:
        for comuna in inmuebles_por_comuna:
            comuna_nombre = comuna['comuna']
            archivo.write(f"Inmuebles en comuna: {comuna_nombre}\n")
            inmuebles = Inmueble.objects.filter(comuna=comuna_nombre)
            
            for inmueble in inmuebles:
                archivo.write(f"Nombre: {inmueble.nombre}\nDescripción: {inmueble.descripcion}\n\n")
            archivo.write("\n")  # Espacio entre comunas

# Llamar a la función
consultar_inmuebles_por_comuna()


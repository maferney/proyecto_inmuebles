import os
import django
import sys

# Añadir el directorio principal de tu proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inmobiliaria.settings')
django.setup()
# Importar el modelo de Inmueble
from inmuebles.models import Inmueble

# Consultar los inmuebles de tipo 'arriendo' y agrupar por región (comuna)
inmuebles_por_region = Inmueble.objects.values('comuna__region', 'nombre', 'descripcion')

# Guardar los resultados en un archivo de texto
with open('inmuebles_por_region.txt', 'w') as file:
    for inmueble in inmuebles_por_region:
        # Escribir el nombre de la región (comuna), nombre del inmueble y descripción
        file.write(f"Región: {inmueble['comuna__region']}\n")
        file.write(f"Nombre: {inmueble['nombre']}\n")
        file.write(f"Descripción: {inmueble['descripcion']}\n")
        file.write('-' * 50 + '\n')

print("Consulta para inmuebles por región realizada y guardada en 'inmuebles_por_region.txt'")
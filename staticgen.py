"""
Generador de página estática a partir de la aplicación Flask
Este script ejecuta la aplicación Flask y guarda la salida como archivo HTML estático
"""
from app import app
import os

# Crear carpeta docs si no existe
if not os.path.exists('docs'):
    os.makedirs('docs')

# Obtener el HTML renderizado de la página principal
with app.test_client() as test_client:
    response = test_client.get('/')
    html_content = response.data.decode('utf-8')

# Guardar como index.html en la carpeta docs
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("¡Página estática generada con éxito en docs/index.html!")
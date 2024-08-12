import os
import re
import time

# Obtener la ruta del directorio donde se encuentra el script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construir las rutas completas de los archivos
following_file_path = os.path.join(current_directory, 'following.html')
followers_file_path = os.path.join(current_directory, 'followers_1.html')

# Leer los archivos y almacenar en conjuntos
with open(following_file_path, 'r') as file:
    following_html = file.read()

with open(followers_file_path, 'r') as file:
    followers_html = file.read()

# Function to extract usernames from HTML content
def extract_usernames(html_content):
    # Use regex to find all Instagram usernames in the href attribute of anchor tags
    return set(re.findall(r'href="https://www.instagram.com/([^/"]+)"', html_content))

# Extract usernames
following_usernames = extract_usernames(following_html)
followers_usernames = extract_usernames(followers_html)

# Find the difference: people followed who are not following back
not_following_back = following_usernames - followers_usernames
#not_following_back = following_usernames
#not_following_back = followers_usernames
#not_following_back = followers_usernames -following_usernames
# Write the result to a file
with open(os.path.join(current_directory, 'not_following_back.txt'), 'w') as file:
    for username in sorted(not_following_back):
        file.write(username + '\n')

# Convertir los usernames a enlaces de Instagram
with open('not_following_back.txt', 'r') as f_in, open('output.txt', 'w') as f_out:
    for line in f_in:
        line = line.strip()
        f_out.write(f'https://www.instagram.com/{line}\n')

# Configuración del tamaño del grupo
tamaño_grupo = 50  # Cambia este número al tamaño del grupo que prefieras

# Leer enlaces desde el archivo y abrirlos en Edge por grupos
with open('output.txt', 'r') as f_out:
    enlaces = [line.strip() for line in f_out if line.strip()]
    
    # Dividir los enlaces en grupos
    for i in range(0, len(enlaces), tamaño_grupo):
        grupo = enlaces[i:i + tamaño_grupo]
        
        # Abrir cada enlace del grupo
        for link in grupo:
            os.startfile(link)
            time.sleep(0.5)  # Pausa de 3 segundos entre cada enlace
        
        # Esperar la orden para continuar con el siguiente grupo
        input("Presiona Enter para continuar con el siguiente grupo...")
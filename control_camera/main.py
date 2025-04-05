import os
import json
from utils import check_camera


# Cargamos el archivo JSON que contiene las rutas
with open('path.json','r') as file:
    data = json.load(file)

# Cargamos el archivo JSON con los id de cámaras
with open('cam_id.json', 'r') as file:
    cam_data = json.load(file)

usuario_actual = os.getenv("USER")

ruta_template = data["paths"][0]

id_template = cam_data["sup_cam"][0]
          
print(check_camera(usuario_actual, id_template, cam_data, data))






# Ahora que tengo el nombre de usuario, procederé a crear la carpeta dentro de /home/ByCarlitag
home_dir = os.path.expanduser(f"~{usuario_actual}")
videos_folder_path = os.path.join(home_dir, "videos")

# Verificar si la carpeta ya existe, si no, crearla
if not os.path.exists(videos_folder_path):
    os.makedirs(videos_folder_path)

videos_folder_path  # Devolvemos la ruta completa de la carpeta creada.


import os
import json
import shutil
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

dowload_path = check_camera(usuario_actual, id_template, cam_data, data)




# Obtener la ruta del directorio actual del proyecto
project_dir = os.getcwd()  # Obtiene el directorio actual del proyecto
videos_folder_path = os.path.join(project_dir, "videos")
# Verificar si la carpeta ya existe, si no, crearla
if not os.path.exists(videos_folder_path):
    os.makedirs(videos_folder_path)


if os.path.exists(dowload_path):
    # Copiar todo el contenido (archivos y subcarpetas) de la carpeta de origen a la carpeta de destino
    try:
        # shutil.copytree() copia directorios completos
        shutil.copytree(dowload_path, videos_folder_path)
        print(f"Todo el contenido se ha copiado a: {videos_folder_path}")
    except Exception as e:
        print(f"Error al copiar los archivos: {e}")
else:
    print("La carpeta de origen no existe.")    


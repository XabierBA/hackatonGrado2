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

dowload_path = os.path.join(check_camera(usuario_actual, id_template, cam_data, data), "DCIM")



# Obtener la ruta del directorio actual del proyecto
project_dir = os.getcwd()  # Obtiene el directorio actual del proyecto
videos_folder_path = os.path.join(project_dir, "videos")
# Verificar si la carpeta ya existe, si no, crearla
if not os.path.exists(videos_folder_path):
    os.makedirs(videos_folder_path)


if os.path.exists(dowload_path):
    try:
        # Filtrar archivos .mp3 y .csv
        files_to_copy = [f for f in os.listdir(dowload_path) if f.endswith(".mp3") or f.endswith(".gcsv")]

        if files_to_copy:
            for file_name in files_to_copy:
                src_file = os.path.join(dowload_path, file_name)
                dest_file = os.path.join(videos_folder_path, file_name)
                
                # Si el archivo no existe en la carpeta destino, lo copiamos
                if not os.path.exists(dest_file):
                    shutil.copy2(src_file, dest_file)
                    print(f"Archivo {file_name} copiado a {dest_file}")
                else:
                    print(f"El archivo {file_name} ya existe en la carpeta destino. No se copió.")
            print(f"Se copiaron {len(files_to_copy)} archivos .mp3 y .csv a: {videos_folder_path}")
        else:
            print("No se encontraron archivos .mp3 o .csv en la carpeta de origen.")
    except Exception as e:
        print(f"Error al copiar los archivos: {e}")
else:
    print("La carpeta de origen no existe.")


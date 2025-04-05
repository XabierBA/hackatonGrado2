import os
import json
from utils import logger, copy_files


# Cargamos el archivo JSON que contiene las rutas
with open('path.json','r') as file:
    data = json.load(file)

# Cargamos el archivo JSON con los id de cámaras
with open('cam_id.json', 'r') as file:
    cam_data = json.load(file)

usuario_actual = os.getenv("USER")

ruta_template = data["paths"][0]

id_template = cam_data["sup_cam"][0]
          
print(logger(usuario_actual, id_template, cam_data, data))

copy_files(usuario_actual, id_template, cam_data, data)
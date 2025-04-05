import os
import json
from utils import check_camera
from datetime import datetime

# Cargamos el archivo JSON que contiene las rutas
with open('path.json','r') as file:
    data = json.load(file)

# Cargamos el archivo JSON con los id de cámaras
with open('cam_id.json', 'r') as file:
    cam_data = json.load(file)

usuario_actual = os.getenv("USER")

ruta_template = data["paths"][0]
id_template = cam_data["sup_cam"][0]

# Verificamos si la carpeta 'logs' existe, si no, la creamos
if not os.path.exists('logs'):
    os.makedirs('logs')

# Obtenemos el timestamp actual
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Ejecutamos la función check_camera
result = check_camera(usuario_actual, id_template, cam_data, data)

# Definimos el archivo de log
log_file = 'logs/check_camera_log.txt'

# Escribimos el resultado con timestamp en el archivo de log
with open(log_file, 'a') as log:
    log.write(f"{timestamp} - {result}\n")
    
print(result)  # También puedes imprimir el resultado en la consola si es necesario

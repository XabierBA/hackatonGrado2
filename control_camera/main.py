import os
import json
from utils import copy_files,obtener_dispositivos_conectados,verificar_numero_serie



# Cargamos el archivo JSON que contiene las rutas
with open('path.json','r') as file:
    data = json.load(file)

# Cargamos el archivo JSON con los id de cámaras
with open('cam_id.json', 'r') as file:
    cam_data = json.load(file)

with open('accepted_serial.json', 'r') as file:
    serial = json.load(file)

usuario_actual = os.getenv("USER")

ruta_template = data["paths"][0]

id_template = cam_data["sup_cam"][0]

serial_template = serial["serials"][0]

devices = obtener_dispositivos_conectados()

for serial_template in serial["serials"]:
    print(f"Verificando el número de serie: {serial_template}")
    verificar_numero_serie(devices, serial_template, usuario_actual, id_template, cam_data, data)

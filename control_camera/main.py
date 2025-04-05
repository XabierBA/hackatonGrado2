import os
import json

from utils import write_log,obtener_dispositivos_conectados,verificar_numero_serie

# Cargamos el archivo JSON que contiene las configuraciones
with open('config.json','r') as file:
    data = json.load(file)


usuario_actual = os.getenv("USER")

ruta_template = data["paths"][0]

id_template = data["sup_cam"][0]

serial_template = data["serials"][0]

devices = obtener_dispositivos_conectados()

verificar_numero_serie(usuario_actual, data)


import os
import json
from pathlib import Path

# Cargamos el archivo JSON que contiene las rutas
with open('path.json','r') as file:
    data = json.load(file)

# Cargamos el archivo JSON con los id de cámaras
with open('cam_id.json', 'r') as file:
    cam_data = json.load(file)

usuario_actual = os.getenv("USER")

ruta_template = data["paths"][0]

for ruta_template in data["paths"]:
    path = ruta_template.format(usuario=usuario_actual, id_camara=id_camara)

    if Path(path).is_dir():
        print(f"La ruta es válida: {path}")
        break

    else:
        print("Ninguna ruta existe")
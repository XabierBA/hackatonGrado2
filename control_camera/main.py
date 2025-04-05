import os
import json
from pathlib import Path
with open('path.json','r') as file:
    data = json.load(file)

usuario_actual = os.getenv("USER")

id_camara = "9C33-6BBD"

for ruta_template in data["paths"]:
    path = ruta_template.format(usuario=usuario_actual, id_camara=id_camara)

    if Path(path).is_dir():
        print(f"La ruta es válida: {path}")
        break

    else:
        print("Ninguna ruta existe")
import os
from pathlib import Path

usuario_actual = os.getenv("USER")

id_camara = "9C33-6BBD"

path = Path(f"/media/{usuario_actual}/{id_camara}/DCIM")

if path.is_dir():
    print("La ruta existe")
else:
    print("La ruta no existe")
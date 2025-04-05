from pathlib import Path
# Recorremos los json comprobando si la camara está conectada mediante el path

def check_camera(usuario_actual, id_template, cam_data, data):
    for id_template in cam_data["sup_cam"]:    
        for ruta_template in data["paths"]:

            # Formateamos la ruta con el usuario y el id de cámara
            path = ruta_template.format(usuario=usuario_actual, id_camara=id_template)
            if Path(path).is_dir():
                return path
  
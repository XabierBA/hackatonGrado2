from pathlib import Path
from time import sleep
from datetime import datetime
import os
import shutil
import subprocess
# Recorremos los json comprobando si la camara está conectada mediante el path

def check_cam_path(usuario_actual, id_template, cam_data, data):
    for id_template in cam_data["sup_cam"]:    
        for ruta_template in data["paths"]:

            # Formateamos la ruta con el usuario y el id de cámara
            path = ruta_template.format(usuario=usuario_actual, id_camara=id_template)
            if Path(path).is_dir():
                return path

def logger(usuario_actual, id_template, cam_data, data):
    # Verificamos si la carpeta 'logs' existe, si no, la creamos
    if not os.path.exists('logs'):
        os.makedirs('logs')

    flag = True
    while flag:
        # Obtenemos el timestamp actual
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ejecutamos la función check_camera
        result = check_cam_path(usuario_actual, id_template, cam_data, data)

        # Definimos el archivo de log
        log_file = 'logs/check_camera_log.txt'

        # Determinamos el mensaje a registrar
        if result:
            flag = False
            log_message = f"{timestamp} - OK: {result}\n"  # Si la función devuelve una ruta
        else:
            flag = True
            log_message = f"{timestamp} - NOT FOUND or NON SUPPORTED CAMERA\n"  # Si la función devuelve None

        # Escribimos el resultado con timestamp en el archivo de log
        with open(log_file, 'a') as log:
            log.write(log_message)

        print(result)  # También puedes imprimir el resultado en la consola si es necesario
        sleep(5)  # Espera 5 segundos antes de la siguiente verificación


def copy_files(usuario_actual, id_template, cam_data, data):

    dowload_path = os.path.join(check_cam_path(usuario_actual, id_template, cam_data, data), "DCIM")



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

def obtener_dispositivos_conectados():
    # Listar todos los dispositivos en /dev/ que sean discos (e.g., /dev/sd*)
    dispositivos = [f for f in os.listdir('/dev') if f.startswith('sd')]
    return dispositivos


def verificar_numero_serie(devices, numero_serie, usuario_actual, id_template, cam_data, data):
    for device in devices:
        dev_path = f"/dev/{device}"
    try:
        # Ejecutamos el comando udevadm para obtener la información del dispositivo
        comando = f"udevadm info -a -p $(udevadm info -q path -n {dev_path})"
        resultado = subprocess.check_output(comando, shell=True, text=True)
        
        # Verificamos si el dispositivo tiene el atributo de número de serie
        if f'ATTRS{{serial}}' not in resultado:
            print(f"No se encontró un dispositivo conectado en {dev_path}.")
        elif f'ATTRS{{serial}}=="{numero_serie}"' in resultado:
            print(f"El dispositivo {dev_path} coincide con el número de serie {numero_serie}.")
            print(logger(usuario_actual, id_template, cam_data, data))
            copy_files(usuario_actual, id_template, cam_data, data)
        else:
            print(f"El dispositivo {dev_path} está conectado, pero el número de serie no coincide.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
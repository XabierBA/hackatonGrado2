from pathlib import Path
from time import sleep
from datetime import datetime
import os
import shutil
import subprocess
import json
# Recorremos los json comprobando si la camara está conectada mediante el path

def check_cam_path(serial):
    try:
        # Buscar todos los dispositivos en /dev/disk/by-id/
        by_id_path = "/dev/disk/by-id/"
        for entry in os.listdir(by_id_path):
            full_path = os.path.join(by_id_path, entry)
            if os.path.islink(full_path):
                if serial in entry:
                    # Obtener el dispositivo real (resolviendo el symlink)
                    device = os.path.realpath(full_path)

                    # Usar lsblk para obtener el punto de montaje
                    result = subprocess.run(['lsblk', '-no', 'MOUNTPOINT', device],
                                            stdout=subprocess.PIPE, text=True)
                    mountpoint = result.stdout.strip()
                    if mountpoint:
                        return mountpoint
                    else:
                        print(f"El dispositivo {device} no está montado.")
                        
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    

# Esta función se encarga de escribir en el archivo de log cuando la llamemos desde otras funciones
def write_log(message):
    # Verificamos si la carpeta 'logs' existe, si no, la creamos
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Definimos el archivo de log
    log_file = 'logs/check_camera_log.txt'

    # Escribimos el mensaje en el archivo de log
    with open(log_file, 'a') as log:
        log.write(f"{message} \n")
        print(message)  # También puedes imprimir el mensaje en la consola si es necesario

def copy_files(usuario_actual,serial, data):
    cam_path = check_cam_path(serial)
    write_log(f"Ruta de la cámara: {cam_path}")

    if not cam_path:
        write_log("No se encontró una ruta válida para la cámara.")
        verificar_numero_serie(usuario_actual, data)
        
    dowload_path = os.path.join(cam_path, "DCIM")

    # Obtener la ruta del directorio actual del proyecto
    project_dir = os.getcwd()  # Obtiene el directorio actual del proyecto
    videos_folder_path = os.path.join(project_dir, "videos")
    # Verificar si la carpeta ya existe, si no, crearla
    if not os.path.exists(videos_folder_path):
        os.makedirs(videos_folder_path)

    if os.path.exists(dowload_path):
        try:
            # Filtrar archivos .mp3 y .csv
            files_to_copy = [f for f in os.listdir(dowload_path) if f.endswith(".MP4") or f.endswith(".gcsv")]

            if files_to_copy:
                for file_name in files_to_copy:
                    src_file = os.path.join(dowload_path, file_name)
                    dest_file = os.path.join(videos_folder_path, file_name)
                    
                    # Si el archivo no existe en la carpeta destino, lo copiamos
                    if not os.path.exists(dest_file):
                        shutil.copy2(src_file, dest_file)
                        write_log(f"Archivo {file_name} copiado a {dest_file}")

                    else:
                        write_log(f"El archivo {file_name} ya existe en la carpeta destino. No se copió.")

                write_log(f"Se copiaron {len(files_to_copy)} archivos .mp4 y .csv a: {videos_folder_path}")
                return False

            else:
                write_log("No se encontraron archivos .mp4 o .gcsv en la carpeta de origen.")
                verificar_numero_serie(usuario_actual,  data)

        except Exception as e:
            write_log(f"Error al copiar los archivos: {e}")
            verificar_numero_serie(usuario_actual,  data)

    else:
        write_log("La carpeta de origen no existe.")
        verificar_numero_serie(usuario_actual, data)


# Esta funcion lista los dispositivos conectados al sistema
def obtener_dispositivos_conectados():
    dispositivos = []
    # Recorremos todos los dispositivos en /sys/block (discos reales)
    for dev in os.listdir('/sys/block'):
    # Saltamos el disco principal (por ejemplo, sda)
        if dev.startswith('sd'):
            ruta_removable = f"/sys/block/{dev}/removable"
            try:
                with open(ruta_removable, 'r') as f:
                    if f.read().strip() == "1":
                        dispositivos.append(dev)
            except FileNotFoundError:
                continue
    return dispositivos



# Esta funcion busca dispositivos en el sistema recibiendo la lista de estes de la funcion anterior con el objetivo de comparar los serial con los registrados como aceptados

def verificar_numero_serie(usuario_actual,  data):
    sleep(5)
    with open('config.json', 'r') as file:
        serial = json.load(file)

    serial_template = serial["serials"][0]
    devices = obtener_dispositivos_conectados()

    for serial_template in serial["serials"]:
        write_log(print(f"Verificando el número de serie: {serial_template}"))   
        flag = True
        while flag:
            
            if not devices:
                write_log("No se encontraron dispositivos conectados.")
                devices = obtener_dispositivos_conectados()
                sleep(5)  # Espera 5 segundos antes de la siguiente verificación
            else:
                flag = False
        for device in devices:
            dev_path = f"/dev/{device}"
        try:
            # Ejecutamos el comando udevadm para obtener la información del dispositivo
            comando = f"udevadm info -a -p $(udevadm info -q path -n {dev_path})"
            resultado = subprocess.check_output(comando, shell=True, text=True)
            
            # Verificamos si el dispositivo tiene el atributo de número de serie
            if f'ATTRS{{serial}}' not in resultado:
                write_log(f"No se encontró un dispositivo conectado en {dev_path}.")
                verificar_numero_serie(usuario_actual,  data)
                 
                
                
            elif f'ATTRS{{serial}}=="{serial_template}"' in resultado:
                write_log(f"El dispositivo {dev_path} coincide con el número de serie {serial_template}.")
                copy_files(usuario_actual,serial_template,data)
            else:
                write_log(f"El dispositivo {dev_path} está conectado, pero el número de serie no coincide.")
                verificar_numero_serie(usuario_actual,  data)
            
        except subprocess.CalledProcessError as e:
            write_log(f"Error al ejecutar el comando: {e}")


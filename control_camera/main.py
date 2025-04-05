import os
import json
from utils import write_log,obtener_dispositivos_conectados,verificar_numero_serie, stabilize_all_with_gyroflow

# Cargamos el archivo JSON que contiene las configuraciones (config.json), para poteriormente usar los datos 
with open('config.json','r') as file:
    data = json.load(file)

# Obtenemos el nombre de usuario del USER qu ejecuta
usuario_actual = os.getenv("USER")

# Obtenemos la ruta en la que pueden estar montada la camara
ruta_template = data["paths"][0]

# Obtenemos los números de serie de los dispositivos permitidos
serial_template = data["serials"][0]

devices = obtener_dispositivos_conectados()




if "__main__" == __name__:
    write_log("Ejecutando el script principal.")

    # Aquí puedes llamar a otras funciones o ejecutar el código principal del programa
    while True:
        verificar_numero_serie(usuario_actual, data)

    #stabilize_all_with_gyroflow()
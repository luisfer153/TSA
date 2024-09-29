import shutil
import subprocess
import requests
import os
import sys
import time
from colorama import Fore, Style, init
from colorama import Fore, Style
import mediafire_dl
import zipfile
import rarfile


# Inicializa colorama
init(autoreset=True)

# Definición de colores para el efecto arcoíris
colores = [
    Fore.RED, Fore.YELLOW, Fore.GREEN,
    Fore.CYAN, Fore.BLUE, Fore.MAGENTA
]

# Función para imprimir el título ASCII con efecto arcoíris
def efecto_arcoiris(titulo_ascii):
    for _ in range(2):  # Muestra el efecto arcoíris 2 veces
        for color in colores:
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la consola
            print(color + titulo_ascii)
            time.sleep(0.2)  # Controla la velocidad del cambio de color

# Función para instalar dependencias

    

    
    


def cerrar_serveo():

    try:
        subprocess.run(['tmux', 'kill-server'], check=True)
        print("Se ha cerrado serveo")
    except subprocess.CalledProcessError as e:
        # Si el comando devuelve un error
        print(f"\n{Fore.RED}Nunca inciaste serveo o ngrok")
        time.sleep(3)
        


# Función para agregar el repositorio de Tailscale
def agregar_repositorio_tailscale():
    try:
        subprocess.run('curl -fsSL https://tailscale.com/install.sh | sh', check=True, shell=True)
        print('Tailscale instalado correctamente.')
    except subprocess.CalledProcessError as e:
        print(f'Error al agregar Tailscale: {e}')

def agregar_ngrok():
    try:
        subprocess.run('curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok', check=True, shell=True)
        print('ngrok instalado')
    except subprocess.CalledProcessError as e:
        print(f'Error al agregar ngrok: {e}')


# Función para establecer permisos en el archivo
def establecer_permisos(archivo):
    try:
        subprocess.run(['chmod', '+x', archivo], check=True)
        print(f'Permisos establecidos para: {archivo}')
    except subprocess.CalledProcessError as e:
        print(f'Error al establecer permisos: {e}')

def cambiar_servidor(archivo_txt, servidor):
    # Lee el contenido actual del archivo
    lineas = []
    if os.path.exists(archivo_txt):
        with open(archivo_txt, "r") as archivo:
            lineas = archivo.readlines()

    # Sobrescribir la configuración del servidor
    with open(archivo_txt, "w") as archivo:
        servidor_existente = False
        
        for linea in lineas:
            if 'server:' in linea:
                archivo.write(f'server:{servidor}\n')  # Actualiza la línea del servidor
                servidor_existente = True
            else:
                archivo.write(linea)

        if not servidor_existente:  # Si no existía, añadimos la configuración del servidor
            archivo.write(f'server:{servidor}\n')


# Uso de la función
def actualizar_archivo(archivo):
    lineas = []
    server_encontrado = False
    
    # Leer el archivo y buscar la línea que contiene "server:"
    with open(archivo, 'r') as f:
        for linea in f:
            if "server:" in linea:
                lineas.append("server:2\n")  # Sobrescribir la línea
                server_encontrado = True
            else:
                lineas.append(linea)  # Mantener la línea original
    
    # Si no se encontró "server:", agregarlo al final
    if not server_encontrado:
        lineas.append("server:2\n")

    # Escribir el contenido actualizado de vuelta al archivo
    with open(archivo, 'w') as f:
        f.writelines(lineas)




def abrirserveo():
# Nombre del archivo donde se guardará la salida
    output_file = 'serveoip.log'
    
    # Crear el archivo vacío si no existe
    if not os.path.exists(output_file):
        open(output_file, 'w').close()

    # Comando que quieres ejecutar en una nueva sesión de tmux
    comando = f"ssh -R 0:localhost:7777 serveo.net > {output_file} 2>&1"

    # Inicia una nueva sesión de tmux y redirige la salida a un archivo
    subprocess.Popen(['tmux', 'new-session', '-d', 'bash', '-c', comando])
    
    # Crear la ruta relativa al archivo de log
    log_file_path = os.path.join(os.path.dirname(__file__), output_file)

    time.sleep(1)

    try:
        with open(log_file_path, 'r') as log_file:
            contenido = log_file.read()  # Leer todo el contenido del archivo
            print(contenido)  # Imprimir el contenido
            print(f"{Fore.CYAN}\npuedes revisar la ip en el archivo 'servoip.log'")
            time.sleep(3)
    except FileNotFoundError:
        print(f"El archivo {log_file_path} no existe.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
  

def abrir_ngrok():
    # Crear o usar una sesión de tmux llamada 'ngrok_session'
    session_name = 'ngrok_session'
    
    # Comando para ejecutar ngrok y redirigir la salida a 'serverip.txt'
    comando = 'ngrok tcp 7777 > serverip.txt 2>&1'
    
    # Iniciar el proceso en tmux
    subprocess.run(['tmux', 'new-session', '-d', '-s', session_name, 'bash', '-c', comando])
    
    print("Se ha abierto el server de ngrok.\nPuedes volver a ver la IP en el txt que se llama 'serverip.txt'.")

    time.sleep(5)
    

def leer_salida_ngrok():
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        data = response.json()
        # Extraer la dirección IP del primer túnel
        ip_info = data['tunnels'][0]
        ip_publica = ip_info['public_url']

        # Escribir la dirección IP en el archivo serverip.txt
        with open('serverip.txt', 'a') as file:  # Usar 'a' para agregar al final
            file.write(f"Dirección IP pública: {ip_publica}\n")

        print(f"Dirección IP pública: {ip_publica} escrita en serverip.txt")
    except Exception as e:
        print(f"Error al obtener la dirección IP: {e}")
        






# Función principal
def main():
    archivo_txt = 'archivo.txt'

    if os.path.exists(archivo_txt):
        print(f'Ninguna novedad')
        interfaz()

    with open(archivo_txt, 'w') as f:
        f.write('Este archivo fue creado con un propósito divino, no lo borres.\n')


    # Agregar el repositorio de Tailscale
    agregar_repositorio_tailscale()

    # Agregar ngrok

    agregar_ngrok()

    



    # Configura el repositorio


    usuario = 'tModLoader'
    repositorio = 'tModLoader'
    url_releases = f'https://api.github.com/repos/{usuario}/{repositorio}/releases/latest'
    response = requests.get(url_releases)

    if response.status_code == 200:
        latest_release = response.json()
        tmodloader_assets = [asset for asset in latest_release['assets'] if 'tModLoader' in asset['name']]

        if tmodloader_assets:
            first_asset = tmodloader_assets[0]
            download_url = first_asset['browser_download_url']
            archivo_destino = os.path.basename(download_url)
            r = requests.get(download_url)

            if r.status_code == 200:
                with open(archivo_destino, 'wb') as f:
                    f.write(r.content)
                print(f'Descargado: {archivo_destino}')

                directorio_destino = os.path.join(os.getcwd(), 'server')
                os.makedirs(directorio_destino, exist_ok=True)

                if archivo_destino.endswith('.zip'):
                    extraer_zip(archivo_destino, directorio_destino)
                elif archivo_destino.endswith('.rar'):
                    extraer_rar(archivo_destino, directorio_destino)

            else:
                print(f'Error al descargar el archivo: {r.status_code}')
        else:
            print('No hay activos de tModLoader disponibles en la última release.')
    else:
        print(f'Error al obtener la última release: {response.status_code}')

    

    print(Fore.RED + '\n\n :) vuelve a iniciar el archivo para iniciar el server')





def interfaz():
    ascii_art = r"""
        *                                               (              

    ) (  `        (   (           (                *   ))\ )   (      
 ( /( )\))(       )\ ))\       )  )\ )  (  (     ` )  /(()/(   )\     
 )\()((_)()\  (  (()/((_)(  ( /( (()/( ))\ )( ___ ( )(_)/(_)((((_)(   
(_))/(_()((_) )\  ((_)_  )\ )(_)) ((_)/((_(()|___(_(_()(_))  )\ _ )\  
| |_ |  \/  |((_) _| | |((_((_)_  _| (_))  ((_)  |_   _/ __| (_)_\(_) 
|  _|| |\/| / _ / _` | / _ / _` / _` / -_)| '_|    | | \__ \  / _ \   
 \__||_|  |_\___\__,_|_\___\__,_\__,_\___||_|      |_| |___/ /_/ \_\  
    """

    efecto_arcoiris(ascii_art)  # Llama a la función de efecto arcoíris
    

    # Ahora, mostramos el menú
    while True:
        
        print(f"{Fore.RED}Solo puedes tener (1) mundo a la vez si usas la aplicacion. de manera manual se pueden tener varios mira el tutorial para ver como ;){Fore.MAGENTA}| CUIDADO si colocas un nuevo mundo los datos del otro mundo se borraran, primero guardalos {Fore.MAGENTA}lo mismso sucede con los mods {Style.RESET_ALL}")
        print("\n")
        print("1. Iniciar server")
        print(f"2. Programa de conexión |{Fore.CYAN} configura esto primero ")
        print(f"3. Actualizar tmod |{Fore.RED} ojito {Fore.CYAN}| deberas importar tus mundos y tus mods denuevo")
        print(f"4. Importar mundo | {Fore.GREEN}primero sube tu mundo a mediafire | {Style.RESET_ALL}")
        print(f"5. importar mods | {Fore.GREEN}primero sube tus mods a mediafire | {Style.RESET_ALL}")
        print("6. salir")
        
        opcion = input("Selecciona una opción (1-5): ")

        if opcion == '1':
            abrir_server()
        elif opcion == '2':
            conexion()
        elif opcion == '3':
            actualizar_tmod()
        elif opcion == '4':
            importar_mundo()

        elif opcion == '5':
            importar_mods()

        elif opcion == '6':
            print('saliendo....')
            sys.exit()        
    
        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")

def abrir_server():
    # Ruta relativa del script a abrir
    script_path = os.path.join('server', 'start-tModLoaderServer.sh')
    
    try:
        # Ejecutar el script
        subprocess.run(['bash', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error al ejecutar el script: {e}')
    except FileNotFoundError:
        print(f'El archivo {script_path} no se encuentra.')

def conexion():
    print("\n")
    print(f"¿Qué servicio usarás?\n1. ngrok | el más rápido pero es pago\n2. serveo | aguanta muchas personas pero es lento\n3. tailscale | aguanta pocas personas pero es rápido |{Fore.GREEN} recuerda tener la app en tu equipo{Style.RESET_ALL}\n4. Cerrar ngrok y serveo\n5. cerrar tailscale\n6. atras")
    
    opcion3 = input("Selecciona una opción (1-4): ")
    
    if opcion3 == '1': 
        token = input('Pega tu config token de ngrok. Ejemplo:\n"2Pa56EWmwdsfVFHGEW4wWWnSpeG_3TfzL2M"\n:')

        try:
            with open("archivo.txt", "r") as archivo:
                lineas = archivo.readlines()
                
            # Sobrescribir el token si ya existe
            with open("archivo.txt", "w") as archivo:
                token_existente = False
                server_existente = False
                for linea in lineas:
                    if 'ngroktoken:' in linea:
                        archivo.write(f'ngroktoken:"{token}"\n')
                        token_existente = True
                    elif 'server:' in linea:
                        archivo.write('server:1\n')  # Sobrescribe la línea del servidor
                        server_existente = True
                    else:
                        archivo.write(linea)

                if not token_existente:
                    archivo.write(f'ngroktoken:"{token}"\n')
                    print("Token guardado en archivo.txt.")

                if not server_existente:  # Si no existía, añadimos server:1
                    archivo.write('server:1\n')
                    

        except FileNotFoundError:
            # Crear el archivo si no existe
            with open("archivo.txt", "w") as archivo:
                archivo.write(f'ngroktoken:"{token}"\n')
                print("El archivo no existía, pero fue creado con el token.")

                # Añadir el token a ngrok
        subprocess.run(['ngrok', 'config', 'add-authtoken', token], check=True)
        print("Token de ngrok configurado correctamente.")
        abrir_ngrok()
        leer_salida_ngrok()

    elif opcion3 == '2':
        print(f"{Fore.RED}\nSe ha iniciado serveo ya puedes iniciar el server")
        abrirserveo()
        actualizar_archivo('archivo.txt')
        time.sleep(4)
        


    elif opcion3 == '3':
        inciar_tailscale()

    elif opcion3 == '4':
        cerrar_serveo()

    elif opcion3 == '5':
        detener_tailscale()

    elif opcion3 == '6':
        interfaz()

    else:
        print("Opción inválida. Por favor, selecciona una opción válida.")



def importar_mods(destination_folder='mods'):
    
    # Comprobar y crear la carpeta de destino si no existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        
   

    # Preparar el comando para ejecutar mediafire-dl
    url = input("Coloca tu link de mediafire | la raiz del rar o del el zip debe contener los mods \n:")
    command = ['mediafire-dl', url]
    
    try:
        # Ejecutar el comando
        subprocess.run(command, check=True, cwd=destination_folder)
        print(f'\n{Fore.RED}mods descargados y guardado en {destination_folder}{Style.RESET_ALL}')
        
        # Listar los archivos en la carpeta de destino
        archivos_descargados = os.listdir(destination_folder)

        # Extraer archivos si hay un archivo zip o rar
        for archivo in archivos_descargados:
            archivo_path = os.path.join(destination_folder, archivo)

            # Comprobar si el archivo es un zip
            if archivo.endswith('.zip'):
                with zipfile.ZipFile(archivo_path, 'r') as zip_ref:
                    zip_ref.extractall(destination_folder)
                print(f'{Fore.GREEN}Archivo zip extraído: {archivo}{Style.RESET_ALL}')
                actualizar_mods()
    

                
            # Comprobar si el archivo es un rar
            elif archivo.endswith('.rar'):
                with rarfile.RarFile(archivo_path) as rar_ref:
                    rar_ref.extractall(destination_folder)
                print(f'{Fore.GREEN}Archivo rar extraído: {archivo}{Style.RESET_ALL}')
                actualizar_mods()
                
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error al ejecutar el comando: {e}{Style.RESET_ALL}")
    except zipfile.BadZipFile:
        print(f"{Fore.RED}Error: El archivo {archivo} no es un zip válido.{Style.RESET_ALL}")
    except rarfile.RarCannotExec:
        print(f"{Fore.RED}Error: No se puede ejecutar rar. Asegúrate de que esté instalado.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Se produjo un error: {e}{Style.RESET_ALL}")


def importar_mundo(destination_folder='worlds'):
    formatear_carpeta()
    # Comprobar y crear la carpeta de destino si no existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        

    # Preparar el comando para ejecutar mediafire-dl
    url = input("Coloca tu link de mediafire | El rar o el zip debe contener todos los archivos del mundo en la raiz\n:")
    command = ['mediafire-dl', url]
    
    try:
        # Ejecutar el comando
        subprocess.run(command, check=True, cwd=destination_folder)
        print(f'\n{Fore.RED}Archivo descargado y guardado en {destination_folder}{Style.RESET_ALL}')
        
        # Listar los archivos en la carpeta de destino
        archivos_descargados = os.listdir(destination_folder)

        # Extraer archivos si hay un archivo zip o rar
        for archivo in archivos_descargados:
            archivo_path = os.path.join(destination_folder, archivo)

            # Comprobar si el archivo es un zip
            if archivo.endswith('.zip'):
                with zipfile.ZipFile(archivo_path, 'r') as zip_ref:
                    zip_ref.extractall(destination_folder)
                print(f'{Fore.GREEN}Archivo zip extraído: {archivo}{Style.RESET_ALL}')
        
                actualizar_mundo()
            # Comprobar si el archivo es un rar
            elif archivo.endswith('.rar'):
                with rarfile.RarFile(archivo_path) as rar_ref:
                    rar_ref.extractall(destination_folder)
                print(f'{Fore.GREEN}Archivo rar extraído: {archivo}{Style.RESET_ALL}')
                
                actualizar_mundo()

    except subprocess.CalledProcessError as e:
        print(f'Error al descargar el archivo: {e}')
    except FileNotFoundError:
        print(Fore.RED + "El comando 'mediafire-dl' no se encuentra. Asegúrate de que esté instalado y en tu PATH." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Ocurrió un error: {e}' + Style.RESET_ALL)
    
    except subprocess.CalledProcessError as e:
        print(f'Error al descargar el archivo: {e}')
    except FileNotFoundError:
        print(Fore.RED + "El comando 'mediafire-dl' no se encuentra. Asegúrate de que esté instalado y en tu PATH.")
    except (zipfile.BadZipFile, rarfile.Error) as e:
        print(f'Error al extraer el archivo: {e}')


# Bloque 2: Función para extraer archivos .rar
def extraer_rar(rar_path, destino):
    try:
        with rarfile.RarFile(rar_path) as rf:
            rf.extractall(destino)
            print(f'Archivos extraídos de {rar_path} en: {destino}')
    except rarfile.Error as e:
        print(f'Error al extraer el archivo .rar: {e}')

# Bloque 3: Función para extraer archivos .zip
def extraer_zip(zip_path, destino):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destino)
            print(f'Archivos extraídos de {zip_path} en: {destino}')
    except zipfile.BadZipFile as e:
        print(f'Error al extraer el archivo .zip: {e}')

def formatear_carpeta(destination_folder='worlds'):
    """Elimina el contenido de la carpeta de destino sin eliminar la carpeta en sí."""
    if os.path.exists(destination_folder):
        # Eliminar todos los archivos y carpetas dentro de la carpeta de destino
        for item in os.listdir(destination_folder):
            item_path = os.path.join(destination_folder, item)
            if os.path.isfile(item_path):
                os.remove(item_path)  # Eliminar archivos
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Eliminar directorios
    
def actualizar_mundo(destination_folder='worlds'):
    # Ruta del archivo de configuración
    config_path = '/workspaces/TSA/server/serverconfig.txt'
    
    # Buscar el archivo .wld en la carpeta de destino
    wld_files = [f for f in os.listdir(destination_folder) if f.endswith('.wld')]
    
    if not wld_files:
        print(f"{Fore.RED}No se encontraron archivos .wld en {destination_folder}.{Style.RESET_ALL}")
        return
    
    # Obtener la dirección del primer archivo .wld encontrado
    wld_file = wld_files[0]
    wld_file_path = os.path.abspath(os.path.join(destination_folder, wld_file))
    
    # Leer el contenido del archivo de configuración
    with open(config_path, 'r') as config_file:
        lines = config_file.readlines()

    # Reemplazar la línea existente que comienza con "world="
    for i, line in enumerate(lines):
        if line.startswith("world="):
            lines[i] = f"world={wld_file_path}\n"  # Reemplazar la línea
            break
    else:
        # Si no se encontró una línea existente, agregarla (opcional)
        lines.append(f"world={wld_file_path}\n")

    # Escribir el contenido actualizado de nuevo en el archivo
    with open(config_path, 'w') as config_file:
        config_file.writelines(lines)

    print(f'{Fore.MAGENTA}La dirección del archivo .wld "{wld_file_path}" se ha actualizado en {config_path}.{Style.RESET_ALL}')

def actualizar_mods(destination_folder='mods'):
    # Ruta del archivo de configuración
    config_path = '/workspaces/TSA/server/serverconfig.txt'

    # Obtener la ruta de la carpeta de mods
    mod_folder_path = os.path.abspath(destination_folder)
    
    # Leer el contenido del archivo de configuración
    with open(config_path, 'r') as config_file:
        lines = config_file.readlines()

    # Reemplazar la línea existente que comienza con "modpath="
    for i, line in enumerate(lines):
        if line.startswith("modpath="):
            lines[i] = f"modpath={mod_folder_path}\n"  # Reemplazar la línea
            break
    else:
        # Si no se encontró una línea existente, agregarla (opcional)
        lines.append(f"modpath={mod_folder_path}\n")

    # Escribir el contenido actualizado de nuevo en el archivo
    with open(config_path, 'w') as config_file:
        config_file.writelines(lines)

    print(f'{Fore.MAGENTA}La ruta de los mods se ha actualizado en {config_path}.{Style.RESET_ALL}')


def inciar_tailscale():
    try:
        # Ejecutar el comando 'sudo tailscale up'
        subprocess.Popen(['sudo', 'tailscaled'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{Fore.GREEN}\npresiona Ctrl + click en el enlace\nse incia automatico si ya vinculaste")
        subprocess.run(['sudo', 'tailscale', 'up'], check=True)
        time.sleep(2)
        
    except subprocess.CalledProcessError as e:
        print(f'Error al ejecutar el comando: {e}')
    except FileNotFoundError:
        print('El comando "tailscale" no se encuentra. Asegúrate de que esté instalado.')

def detener_tailscale():
     try:
        
        subprocess.run(['sudo', 'pkill', 'tailscaled'], check=True)
        print(f"{Fore.GREEN}\nse ha detenido tailscale{Style.RESET_ALL}")
        time.sleep(1)

     except subprocess.CalledProcessError as e:
        print(f'\n{Fore.RED}nunca abriste tailcale')
        time.sleep(3)

def actualizar_tmod():
    usuario = 'tModLoader'
    repositorio = 'tModLoader'
    url_releases = f'https://api.github.com/repos/{usuario}/{repositorio}/releases/latest'
    response = requests.get(url_releases)

    if response.status_code == 200:
        latest_release = response.json()
        tmodloader_assets = [asset for asset in latest_release['assets'] if 'tModLoader' in asset['name']]

        if tmodloader_assets:
            first_asset = tmodloader_assets[0]
            download_url = first_asset['browser_download_url']
            archivo_destino = os.path.basename(download_url)
            r = requests.get(download_url)

            if r.status_code == 200:
                with open(archivo_destino, 'wb') as f:
                    f.write(r.content)
                print(f'Descargado: {archivo_destino}')

                directorio_destino = os.path.join(os.getcwd(), 'server')
                os.makedirs(directorio_destino, exist_ok=True)

                if archivo_destino.endswith('.zip'):
                    extraer_zip(archivo_destino, directorio_destino)
                elif archivo_destino.endswith('.rar'):
                    extraer_rar(archivo_destino, directorio_destino)

            else:
                print(f'Error al descargar el archivo: {r.status_code}')
        else:
            print('No hay activos de tModLoader disponibles en la última release.')
    else:
        print(f'Error al obtener la última release: {response.status_code}')

if __name__ == "__main__":
    main()

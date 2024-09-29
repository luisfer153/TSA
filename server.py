import subprocess
import requests
import os
import sys
import time
from colorama import Fore, Style, init
import dependencias
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
    subprocess.run(['tmux', 'kill-server'], check=True)
    print("Se ha cerrado serveo")

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
    comando = "tmux new-session -d 'ssh -R 0:localhost:7777 serveo.net'"
    subprocess.Popen(comando, shell=True)

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

    # Instalar dependencias
    dependencias.instalar_dependencias()

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

    print('\n\n :) vuelve a iniciar el archivo para iniciar el server')







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
        print("\n")
        print("1. Iniciar server")
        print("2. Programa de conexión | configura esto primero ")
        print("3. Actualizar tmod | ojito")
        print("4. Importar mundo | primero sube tu mundo a mediafire")
        print("5. Cancelar")
        
        opcion = input("Selecciona una opción (1-5): ")

        if opcion == '1':
            iniciar_server()
        elif opcion == '2':
            conexion()
        elif opcion == '3':
            actualizar()
        elif opcion == '4':
            print("Volviendo atrás...")
            break  # Salir del bucle y volver atrás

        elif opcion == '5':
            print('saliendo....')
            sys.exit()

    
        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")

def iniciar_server():
    print("\n")
    print("Iniciando el servidor...")
    input("Presiona Enter para continuar...")

def conexion():
    print("\n")
    print("¿Qué servicio usarás?\n1. ngrok | el más rápido pero es pago\n2. serveo | aguanta muchas personas pero es lento\n3. tailscale | aguanta pocas personas pero es rápido\n4. Cerrar serveo :)\n5. cerrar tailscale")
    
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
        print("Se ha iniciado serveo ya puedes iniciar el server")
        abrirserveo()
        actualizar_archivo('archivo.txt')
        


    elif opcion3 == '3':
        print("Configurando Tailscale...")  # Lógica para Tailscale aquí
        # Puedes implementar la lógica de configuración de Tailscale aquí

    elif opcion3 == '4':
        cerrar_serveo()

    else:
        print("Opción inválida. Por favor, selecciona una opción válida.")

def actualizar():
    print("\n")
    print("Actualizando tModLoader...")  # Lógica para actualizar tModLoader aquí
    # Puedes implementar la lógica de actualización de tModLoader aquí

# Bloque 1: Punto de entrada e importaciones


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

if __name__ == "__main__":
    main()
    
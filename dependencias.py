import subprocess
import sys
import colorama
from colorama import Fore, Style

def instalar_dependencias():
    subprocess.run(['sudo', 'apt-get', 'update'], check=True)
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'unrar'], check=True)
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'rarfile'], check=True)
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'tmux'], check=True)
    subprocess.run(['pip3', 'install', 'git+https://github.com/Juvenal-Yescas/mediafire-dl'], check=True)
    subprocess.run("sudo apt-get update && sudo apt-get install -y rar", shell=True, check=True)

    # Imprimir el mensaje en color rojo
    print(Fore.RED + "\nDependencias instaladas, ya puedes ejecutar el server.py")
    print(Style.RESET_ALL)  # Reinicia el estilo al valor por defecto

if __name__ == "__main__":
    colorama.init(autoreset=True)  # Inicializa colorama
    instalar_dependencias()  # Llama a la función para instalar dependencias

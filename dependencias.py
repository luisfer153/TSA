import subprocess
import sys


def instalar_dependencias():
    subprocess.run(['sudo', 'apt-get', 'update'], check=True)
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'unrar'], check=True)
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'rarfile'], check=True)
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'tmux'], check=True)
    subprocess.run(['pip3', 'install', 'git+https://github.com/Juvenal-Yescas/mediafire-dl'], check=True)
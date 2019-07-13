
from Controlador import Controlador
from Downloader import Downloader

if __name__ == '__main__':
    control = Controlador()
    Vista = Downloader(control)
    control.iniciar()

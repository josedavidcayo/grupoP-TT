import os, sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrolladores y para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
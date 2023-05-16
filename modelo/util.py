import pygame as pg
from tkinter import messagebox


def formatearTiempo(seg):
    segundos = seg % 60
    minutos = seg // 60
    tiempo_actual = str(minutos) + ":" + (str(segundos) if segundos > 9 else "0" + str(segundos))
    return tiempo_actual


def obtenerTecla(tecla):
    switcher = {
        pg.K_1: 1,
        pg.K_2: 2,
        pg.K_3: 3,
        pg.K_4: 4,
        pg.K_5: 5,
        pg.K_6: 6,
        pg.K_7: 7,
        pg.K_8: 8,
        pg.K_9: 9,
    }
    return switcher.get(tecla, None)


def mostrarMensaje(titulo, mensaje):
    messagebox.showinfo(titulo, mensaje)

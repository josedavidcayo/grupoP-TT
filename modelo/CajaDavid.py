import pygame
import os

class Caja:
    filas = 9
    columnas = 9
    COLOR_GRIS = (128, 128, 128)
    COLOR_NEGRO = (0, 0, 0)
    COLOR_ROJO = (255, 0, 0)
    COLOR_BLANCO = (255, 255, 255)

    def __init__(self, valor, fila, columna, ancho, altura):
        self.valor = valor  # Valor actual de la caja
        self.temp = 0  # Para indicar los números potenciales que podrían encajar en esta caja
        self.fila = fila
        self.columna = columna
        self.ancho = ancho
        self.altura = altura
        self.seleccionada = False  # Para marcar si esta caja está seleccionada

    # Dibujar esta caja
    def dibujar(self, ventana):
        rutaActual = os.path.dirname(os.path.abspath(__file__))
        rutaFuente = os.path.join(rutaActual, "../fuente/ComicNeue_Bold.otf")
        fuente = pygame.font.Font( rutaFuente, 26)
        espacio = self.ancho / 9

        # Calcular la posición de dibujo relativa a esta caja en el tablero
        x = self.columna * espacio
        y = self.fila * espacio

        if self.temp != 0 and self.valor == 0:
            texto = fuente.render(str(self.temp), 1, self.COLOR_GRIS)
            ventana.blit(texto, (x + 3, y + 3))  # Dibujar el número pequeño en la esquina superior izquierda
        elif self.valor != 0:
            texto = fuente.render(str(self.valor), 1, self.COLOR_BLANCO)
            ventana.blit(texto, (x + (espacio/2 - texto.get_width()/2), y + (espacio/2 - texto.get_height()/2)))  # Dibujar el número en el centro

        if self.seleccionada:
            pygame.draw.rect(ventana, self.COLOR_ROJO, (x, y, espacio, espacio), 3)  # Si esta caja está seleccionada, dibujar un recuadro rojo

    def establecer_valor(self, valor):
        self.valor = valor

    def establecer_temp(self, valor):
        self.temp = valor
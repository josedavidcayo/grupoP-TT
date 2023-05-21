import pygame
import os
import vista.Color as Color

class Caja:
    filas = 9
    columnas = 9
    

    def __init__(self, valor, fila, columna, ancho, altura):
        self.valor = valor  # Valor actual de la caja
        self.temp = 0  # Para indicar los números potenciales que podrían encajar en esta caja
        self.fila = fila
        self.columna = columna
        self.ancho = ancho
        self.altura = altura
        self.seleccionada = False  # Para marcar si esta caja está seleccionada

    # Dibujar esta caja
    def dibujar(self, tablero_surface):
        rutaActual = os.path.dirname(os.path.abspath(__file__))
        rutaFuente = os.path.join(rutaActual, "../fuente/ComicNeue_Bold.otf")
        fuente = pygame.font.Font(rutaFuente, 26)
        espacio = self.ancho / 9

        # Calcular la posición de dibujo relativa a esta caja en el tablero
        x = self.columna * espacio
        y = self.fila * espacio

        if self.temp != 0 and self.valor == 0:
            texto = fuente.render(str(self.temp), 1, Color.gris)
            tablero_surface.blit(texto, (x + 3, y + 3))  # Dibujar el número pequeño en la esquina superior izquierda
        elif self.valor != 0:
            texto = fuente.render(str(self.valor), 1, Color.negro)
            # Ajustar las coordenadas de dibujo para centrar el número en la caja
            texto_x = x + (espacio - texto.get_width()) // 2
            texto_y = y + (espacio - texto.get_height()) // 2
            tablero_surface.blit(texto, (texto_x, texto_y))  # Dibujar el número en el centro

        if self.seleccionada:
            caja_x = self.columna * espacio
            caja_y = self.fila * espacio
            caja_ancho = self.ancho / 9
            caja_alto = self.altura / 9
            pygame.draw.rect(tablero_surface, Color.rojo, (caja_x, caja_y, caja_ancho, caja_alto), 3)
    

    def establecerValor(self, valor):
        self.valor = valor

    def establecerTemp(self, valor):
        self.temp = valor
import pygame
from Tablero import Tablero
from Caja import Caja
import util


class Juego:
    def __init__(self, ancho, altura):
        self.tablero = Tablero()
        self.filas = self.columnas = 9
        self.cajas = [[Caja(self.tablero.tablero[i][j], i, j, ancho, altura) for j in range(9)] for i in range(9)]
        self.ancho = ancho
        self.altura = altura
        self.seleccionada = None

    def colocar(self, valor):
        fila, columna = self.seleccionada
        self.cajas[fila][columna].establecerValor(valor)

    def colocarTemp(self, valor):
        fila, columna = self.seleccionada
        self.cajas[fila][columna].establecerTemp(valor)

    def dibujar(self, tablero_surface):
        espacio = self.ancho / 9
    
        for i in range(self.filas + 1):
            if i % 3 == 0 and i != 0:  # Dibujar bordes más gruesos cada 3x3 cajas
                grosor = 4
            else:
                grosor = 1
            pygame.draw.line(tablero_surface, (255, 255, 255), (0, i * espacio), (self.ancho, i * espacio), grosor)  # Dibujar línea horizontal
            pygame.draw.line(tablero_surface, (255, 255, 255), (i * espacio, 0), (i * espacio, self.altura), grosor)  # Dibujar línea vertical
    
        for i in range(9):
            for j in range(9):
                self.cajas[i][j].dibujar(tablero_surface)

    def seleccionar(self, fila, columna):
        # Restablecer el estado seleccionado de otras cajas
        for i in range(9):
            for j in range(9):
                self.cajas[i][j].seleccionada = False
        fila, columna = int(fila), int(columna)
        self.cajas[fila][columna].seleccionada = True  # Marcar la caja actual como seleccionada
        self.seleccionada = (fila, columna)

    def limpiar(self):
        fila, columna = self.seleccionada

        # Limpiar los atributos de la caja seleccionada
        self.cajas[fila][columna].establecerValor(0)
        self.cajas[fila][columna].establecerTemp(0)

    def click(self, pos):
        if pos[0] < self.ancho and pos[1] < self.altura:  # Verificar si el usuario hizo clic en una posición válida en el tablero
            espacio = self.ancho / 9
            x = (pos[0])  // espacio
            y = (pos[1])// espacio
            return (y, x)
        elif pos[0] <= 60 and pos[1] >= 540:  # Si se hizo clic en el icono '?', mostrar mensaje de ayuda
            ayudaStr = "Presiona 1-9 para ingresar un número\n" \
                        "Presiona ENTER para colocarlo en el tablero\n" \
                        "Presiona BACKSPACE para borrar un número. ¡Diviértete!"
            util.mostrarMensaje("Ayuda", ayudaStr)
        else:
            return None

    def verificarCajaVacia(self):
        for i in range(9):
            for j in range(9):
                if self.cajas[i][j].valor == 0:
                    return True
        return False

    def verificarRespuesta(self):
        self.tablero.resolver()  # Resolver el tablero actual
        for i in range(9):
            for j in range(9):
                if self.tablero.tablero[i][j] != self.cajas[i][j].valor:
                    return False
        return True


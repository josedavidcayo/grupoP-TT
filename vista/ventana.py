import pygame
import time
import util.util as util
import os
from controlador.Juego import Juego


def redibujarVentana(ventana, tablero, tiempo):
    ventana.fill((0, 0, 0))

    bgVentana = pygame.image.load('img/sud-base.png')
    bgVentana = pygame.transform.scale(bgVentana, ventana.get_size())
    ventana.blit(bgVentana, (0, 0))

    tablero_surface = pygame.Surface((400, 400))
    tablero_surface.fill((255, 255, 255))
    tablero.dibujar(tablero_surface)

    #Btn cerrar
    #Agregar img de boton cerrar.

    ventana.blit(tablero_surface, (50, 130))

    rutaActual = os.path.dirname(os.path.abspath(__file__))
    rutaFuente = os.path.join(rutaActual, "../fuente/ComicNeue_Bold.otf")
    fuente = pygame.font.Font(rutaFuente, 26)
    textoTiempo = fuente.render("Tiempo: " + util.formatearTiempo(tiempo), 1, (0, 0, 0))
    ventana.blit(textoTiempo, (20, 555))  # Dibujar el tiempo en la esquina inferior izquierda


def main():
    tamanioVentana = (800, 600)
    ventana = pygame.display.set_mode(tamanioVentana)
    pygame.display.set_caption("Sudoku MDI")

    juego = Juego(400, 400)
    corriendo = True
    teclaPresionada = None
    inicio = time.time()

    while corriendo:
        tiempoActual = round(time.time() - inicio)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if util.obtenerTecla(evento.key) is not None:
                    teclaPresionada = util.obtenerTecla(evento.key)
                elif evento.key == pygame.K_BACKSPACE:
                    juego.limpiar()
                    teclaPresionada = None
                elif evento.key == pygame.K_RETURN:
                    x, y = juego.seleccionada
                    juego.colocar(teclaPresionada)
                elif evento.key == pygame.K_TAB:
                    if juego.verificarCajaVacia() is False and juego.verificarRespuesta() is True:
                        mensajeFinal = "Has completado el tablero en " + util.formatearTiempo(tiempoActual) + \
                                       "\nPresiona OK para iniciar un nuevo juego"
                        util.mostrarMensaje("¡Tablero completado!", mensajeFinal)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x=pos[0] - 50
                y=pos[1] -130
                clickeado = juego.click((x,y))
                print(str(pos) + "   " + str(clickeado))
                if clickeado:
                    juego.seleccionar(clickeado[0], clickeado[1])
                    teclaPresionada = None
        if juego.seleccionada and teclaPresionada is not None:
            juego.colocarTemp(teclaPresionada)

        redibujarVentana(ventana, juego, tiempoActual)

        pygame.display.update()




import pygame, sys
from pygame.locals import *

pygame.init()

PANTALLA=pygame.display.set_mode((400,400))
pygame.display.set_caption("Mi primer ventana vacia")

fuente = pygame.font.SysFont("Arial",20,False,False)
fila = None
columna=None

tablero = [[0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0]]



for i in range(9):
    for j in range(9):
        pygame.draw.rect(PANTALLA,(255,255,255),(j*40,i*40,40,40),1)



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9 and fila is not None and columna is not None:
                tablero[fila][columna]=event.key - pygame.K_0
                fila= None
                columna= None

        elif event.type==pygame.MOUSEBUTTONDOWN:
            x,y=pygame.mouse.get_pos()
            fila=y // 40
            columna=x //40
            print(fila,columna)
            print(tablero[fila][columna])
            
            #Falta borrar numero cuando se quiere cambiar el valor
            
                

    for i in range(9):
        for j in range(9):
            if tablero[i][j]!=0:
                num=tablero[i][j]
                texto = fuente.render(str(num),True, (255,111,145))
                PANTALLA.blit(texto,(j*40+15,i*40+10))
                

    pygame.display.update()
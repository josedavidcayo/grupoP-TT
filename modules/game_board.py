import pygame
import copy

from utils.sudoku_solver import SudokuBoard
from utils.tools import resource_path
from utils.constants import *

class GameBoard:
    def __init__(self, menu, theme):
        self._active = False
        self.timer = None
        self.count_up = None

        self.menu = menu
        self.theme = theme

        self.board = [[0] * 9 for _ in range(9)]
        self.backbutt_img = pygame.transform.scale(pygame.image.load(resource_path('img/left.png')).convert_alpha(), (30, 30))
        self.restartbutt_img = pygame.transform.scale(pygame.image.load(resource_path('img/restart.png')).convert_alpha(), (36, 36))
        self.donebutt_img = pygame.transform.scale(pygame.image.load(resource_path('img/done.png')).convert_alpha(), (36, 36))
        self.back_button = None

        # fuente básica
        self.base_font = pygame.font.Font(None, 32)

        self.sc = SudokuBoard()
        self.unfinished_board = []
        self.unfinished_boardcopy = []
        self.solved_board = []
        self.input_num = []
        self.reset_button = []
        self.insta_solve_button = []
        self.insta_solve = False
        self.popup_menu = []
        self.popup_replay = []
        self.difficulty = ''
        self.selected_circle = []
        # teclas para el juego
        self.set_keys = {0: [pygame.K_0, pygame.K_KP0, pygame.K_DELETE, pygame.K_BACKSPACE],
                         1: [pygame.K_1, pygame.K_KP1], 2: [pygame.K_2, pygame.K_KP2],
                         3: [pygame.K_3, pygame.K_KP3], 4: [pygame.K_4, pygame.K_KP4],
                         5: [pygame.K_5, pygame.K_KP5], 6: [pygame.K_6, pygame.K_KP6],
                         7: [pygame.K_7, pygame.K_KP7], 8: [pygame.K_8, pygame.K_KP8],
                         9: [pygame.K_9, pygame.K_KP9]}

        return

    def oncall(self, diff: str = "Principiante"):
        """Establece la dificultad del tablero y, si no está activo, dibuja el tablero"""
        self.difficulty = diff
        if not self._active:
            self.drawlayout()
        self._active = True
        return self._active

    def drawlayout(self):
        """Método para volver a dibujar el tablero"""
        self.drawboard()
        self.backbutton()
        theme.themebutton()

    def endgame(self):
        """Función para limpiar todas las variables y finalizar el juego actual"""
        self.__init__()
        menu.startgame = False

    def backbutton(self):
        """Dibuja el botón de atrás en el tablero"""
        self.back_button = pygame.draw.circle(surface, safety_secondary_color, (25, 25), 20)
        surface.blit(self.backbutt_img, self.backbutt_img.get_rect(center=self.back_button.center))
        return

    def counter(self):
        """Contador del tiempo dedicado a intentar resolver el sudoku"""
        if self.timer is None:
            self.timer = time.time()
        self.count_up = time.time() - self.timer
        return self.count_up

    def solved(self):
        """Función para verificar si el tablero se ha resuelto y devolver un valor booleano"""
        if all(0 not in t for t in self.unfinished_board) and self._active:
            if self.unfinished_board == self.solved_board and self.unfinished_board:
                return True
            for row in range(9):
                for col in range(9):
                    if not self.sc.is_valid(row, col, self.unfinished_board[row][col]):
                        return False
            return True
        return False

    def setnumber(self, row, col, num: int = 20):
        """Función que guarda y muestra el número ingresado en el tablero

        :parametro row: Fila del tablero
        :parametro col: Columna del tablero
        :parametro num: El número que se guarda/muestra
        :return: Nada
        """
        if num != 0 and num != 20:
            self.unfinished_board[row][col] = num
            b = self.board[row][col]
            text_surface = self.base_font.render(str(num), True, safety_base_inverse)
            surface.blit(text_surface, (b.x + (b.width/4+5), b.y + (b.height/4)))
            pygame.display.flip()
        else:
            num = num if num == 0 else self.unfinished_board[row][col]
            if num != 0:
                b = self.board[row][col]
                text_surface = self.base_font.render(str(num), True, safety_base_inverse)
                surface.blit(text_surface, (b.x + (b.width/4+5), b.y + (b.height/4)))
            else:
                self.unfinished_board[row][col] = 0
        return

    def number_animation(self, row: int, col: int, p: int):
        """Esta función anima los números difíciles resueltos y luego establece posiciones vacías
         a cero para evitar que se haga clic

        :parametro row: Fila del tablero
        :parametro col: Columna del tablero
        :parametro p: Tamaño del círculo
        :return: Nada
        """
        q = pygame.draw.circle(surface, hardsolved_circles, ((50 * (col + 1)) - 14, 76 + 50 * row), 0 + p)
        self.board[row][col] = 0
        text_surface = self.base_font.render(str(self.unfinished_board[row][col]), True, safety_base_color)
        surface.blit(text_surface, (q.x + (q.width / 4 + 5), q.y + (q.height / 4)))

    def draw_boardbutton(self):
        """Esta función dibuja números difíciles resueltos y botones de tablero vacíos y los guarda en el tablero."""
        for row in range(10):
            for col in range(10):
                if row != 9 and col != 9:  # circles
                    past_num = int(str(row) + str(col)) in self.input_num
                    board_circle_color = safety_base_color if self.unfinished_board[row][col] == 0 or past_num else color_white

                    if self.insta_solve:
                        if self.unfinished_boardcopy[row][col] == 0:
                            pygame.draw.circle(surface, safety_base_color, ((50 * (col + 1)) - 14, 76 + 50 * row), 20)
                            self.setnumber(row, col, self.solved_board[row][col])
                            pygame.time.delay(80)
                        continue

                    if self.unfinished_board[row][col] != 0 and not past_num:
                        if theme.bar_position:
                            self.number_animation(row, col, 20)
                        else:
                            for p in range(20):
                                self.number_animation(row, col, p)
                                pygame.time.delay(2)
                                pygame.display.flip()
                    else:
                        self.board[row][col] = pygame.draw.circle(surface, board_circle_color, ((50*(col+1)) - 14, 76+50*row), 20)
                        if past_num:
                            self.setnumber(row, col, 20)

        return

    def drawboard(self):
        """Esta función crea el tablero, llama a la función para dibujar los botones del tablero.
        y dibuja el botón de reinicio y resolución instantánea.
        """
        if self.insta_solve:
            self.draw_boardbutton()
            return
        dash_space = 23
        factor = 0.77
        surface.fill(safety_base_color)
        if not self.unfinished_board:
            # generar tablero
            self.solved_board = self.sc.generate()
            self.unfinished_board = self.sc.scrambled_board(self.difficulty)
            self.unfinished_boardcopy = copy.deepcopy(self.unfinished_board)
            # print(*self.solved_board, sep="\n")  # hoja de trucos

        for i in range(0, 10):
            if i % 3 == 0 and i != 0 and i != 9:  # 4 líneas oscuras
                pygame.draw.line(surface, safety_secondary_color, (10 + 50 * i, 50), (10 + 50 * i, 500), 4)  # col
                pygame.draw.line(surface, safety_secondary_color, (10, 50 + 50 * i), (450, 50 + 50 * i), 4)  # row
            for index in range(1, 10):
                if i != 0 and i != 9:
                    # cálculo de línea discontinua de columna
                    col_d = (10 + 50 * i, (50*(index-1+factor)) + dash_space)
                    col_d_end = (10 + 50 * i,  (50*(index+factor)))
                    # cálculo de líneas discontinuas de fila
                    row_d = ((50*(index-1)) + dash_space, 50 + 50 * i)
                    row_d_end = ((50*index), 50 + 50 * i)
                    pygame.draw.line(surface, safety_secondary_color, col_d, col_d_end, 1)
                    pygame.draw.line(surface, safety_secondary_color, row_d, row_d_end, 1)
        self.draw_boardbutton()

        self.reset_button = [pygame.draw.circle(surface, safety_secondary_color, (WIDTH/4 - 50, HEIGHT - HEIGHT/4), 25),
                             pygame.draw.circle(surface, safety_secondary_color, (WIDTH/4 + 50, HEIGHT - HEIGHT/4), 25),
                             pygame.draw.rect(surface, safety_secondary_color, (WIDTH / 4 - 50, HEIGHT - HEIGHT / 4 - 25, 100, 50))]

        self.insta_solve_button = [pygame.draw.circle(surface, safety_secondary_color, (WIDTH - WIDTH/4-50, HEIGHT - HEIGHT/4), 25),
                                   pygame.draw.circle(surface, safety_secondary_color, (WIDTH - WIDTH/4+50, HEIGHT - HEIGHT/4), 25),
                                   pygame.draw.rect(surface, safety_secondary_color, (WIDTH - WIDTH/4-50, HEIGHT - HEIGHT/4-25, 100, 50))]

        surface.blit(self.restartbutt_img, self.restartbutt_img.get_rect(center=self.reset_button[-1].center))
        surface.blit(self.donebutt_img, self.donebutt_img.get_rect(center=self.insta_solve_button[-1].center))

    def highlightbutton(self, row: int, col: int, cir_posx: int, cir_posy: int, hl: bool = False):
        """Función para resaltar posiciones vacías cuando se hace clic.

        :parametro row: Fila del tablero
        :parametro col: Columna del tablero
        :parametro cir_posx: X Posición del círculo resaltado/clic.
        :parametro cir_posy: Y Posición del círculo resaltado/clic.
        :parametro hl: Booleano para resaltar o dejar de resaltar una posición circular.
        :return: Nada
        """
        if not hl:
            for i in range(21):  # dejar de resaltar
                pygame.draw.circle(surface, safety_base_color, (cir_posx, cir_posy), 20)
                pygame.draw.circle(surface, safety_secondary_color, (cir_posx, cir_posy), 20-i)
                if self.board[row][col] != 0:
                    self.setnumber(row, col)
                    pygame.display.update(self.board[row][col])
                    pygame.time.delay(5)
            self.board[row][col] = pygame.draw.circle(surface, safety_base_color, (cir_posx, cir_posy), 20)
        elif hl:
            for i in range(21):  # resaltar
                self.board[row][col] = pygame.draw.circle(surface, safety_secondary_color, (cir_posx, cir_posy), 0+i)
                pygame.display.update(self.board[row][col])
                pygame.time.delay(5)
        self.selected_circle = [self.board[row][col], row, col]
        return

    def end_game_popup(self):
        """Dibuje la ventana emergente del menú final del juego con los botones 'ir al menú principal' y 'resetear'"""
        s = pygame.Surface((480, 800))
        s.set_alpha(50)
        s.fill(safety_base_color)
        surface.blit(s, (0, 0))

        self.popup_menu = [pygame.draw.circle(surface, safety_base_color, (WIDTH / 4 - 50, HEIGHT - HEIGHT / 4), 24),
                           pygame.draw.circle(surface, safety_base_color, (WIDTH / 4 + 50, HEIGHT - HEIGHT / 4), 24),
                           pygame.draw.rect(surface, safety_base_color, (WIDTH / 4 - 50, HEIGHT - HEIGHT / 4 - 24, 100, 48))]

        self.popup_replay = [pygame.draw.circle(surface, safety_base_color, (WIDTH - WIDTH / 4 - 50, HEIGHT - HEIGHT / 4), 24),
                             pygame.draw.circle(surface, safety_base_color, (WIDTH - WIDTH / 4 + 50, HEIGHT - HEIGHT / 4), 24),
                             pygame.draw.rect(surface, safety_base_color, (WIDTH - WIDTH / 4 - 50, HEIGHT - HEIGHT / 4 - 24, 100, 48))]

        pop_menu = self.base_font.render("Menú", True, safety_secondary_color)
        pop_replay = self.base_font.render("Nuevo", True, safety_secondary_color)

        surface.blit(pop_menu, (self.popup_menu[-1].x + (self.popup_menu[-1].width / 4 - 33), self.popup_menu[-1].y + (self.popup_menu[-1].height / 4 + 2)))
        surface.blit(pop_replay, (self.popup_replay[-1].x + (self.popup_replay[-1].width / 4 - 31), self.popup_replay[-1].y + (self.popup_replay[-1].height / 4 + 2)))

        if self.insta_solve:
            solv_text = self.base_font.render("Lo resolvimos por vos para que veas el resultado", True, safety_base_inverse)
            surface.blit(solv_text, (WIDTH / 2 - solv_text.get_width() / 2, HEIGHT - HEIGHT / 3))
        else:
            won_text = self.base_font.render("¡HAS GANADO!", True, safety_base_inverse)
            surface.blit(won_text, (WIDTH / 2 - won_text.get_width() / 2, HEIGHT - HEIGHT / 3))
        pygame.display.flip()
        return True

    def backbutton_event(self, event):
        """Una función para finalizar el juego actual cuando se presiona el botón Atrás"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._active and self.back_button.collidepoint(event.pos):
                self.endgame()
                return False
        return True

    def end_game_popup_action(self, event):
        """Función para que los botones de finalizar el juego regresen al menú principal o comiencen un nuevo juego"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pop_menu = [x for x in self.popup_menu if x.collidepoint(event.pos)]
            replay_menu = [x for x in self.popup_replay if x.collidepoint(event.pos)]
            # print(event.pos, pop_menu, replay_menu)
            if pop_menu:
                self.endgame()
                return False
            elif replay_menu:
                # guardar la vieja dificultad
                diffcultly = self.difficulty
                self.__init__()  # reset
                self.oncall(diffcultly)
                pygame.display.flip()
                return True

    def onkeypress(self, event):
        """Esta función determina si el mouse está presionando un círculo vacío válido, restablecer, resolver el botón o
        si se presiona una tecla numérica válida.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._active:
                board_button_detection = {str(row) + str(col): g for row, d in enumerate(self.board) for col, g in enumerate(d) if g != 0 and g.collidepoint(event.pos)}
                reset_button = [x for x in self.reset_button if x.collidepoint(event.pos)]
                solve_button = [x for x in self.insta_solve_button if x.collidepoint(event.pos)]

                if reset_button:  # botón para restablecer el tablero
                    self.unfinished_board = copy.deepcopy(self.unfinished_boardcopy)
                    self.drawlayout()
                    pygame.display.flip()

                if solve_button and not self.insta_solve:  # haciendo clic en el botón de resolver
                    self.unfinished_board = self.solved_board
                    self.insta_solve = True
                    self.drawlayout()
                    return

                if board_button_detection:  # azulejo del tablero en el que se hizo clic
                    bbd_key = [*board_button_detection][0]
                    row, col = int(bbd_key[0]), int(bbd_key[-1])
                    if self.board[row][col] != 0:
                        cir_posx = board_button_detection[bbd_key].x + board_button_detection[bbd_key].width/2
                        cir_posy = board_button_detection[bbd_key].y + board_button_detection[bbd_key].height/2
                        if self.selected_circle:
                            sc = self.selected_circle[0]
                            select_row = self.selected_circle[1]
                            select_col = self.selected_circle[2]

                            if sc.x == board_button_detection[bbd_key].x and sc.y == board_button_detection[bbd_key].y:
                                self.highlightbutton(row, col, cir_posx, cir_posy, False)
                                self.selected_circle = []
                            elif sc.x != board_button_detection[bbd_key].x or sc.y != board_button_detection[bbd_key].y:
                                old_posx = sc.x + sc.width/2
                                old_posy = sc.y + sc.height/2

                                self.highlightbutton(select_row, select_col, old_posx, old_posy, False)
                                self.highlightbutton(row, col, cir_posx, cir_posy, True)
                                self.setnumber(row, col)
                            else:
                                self.highlightbutton(row, col, cir_posx, cir_posy, True)

                            self.setnumber(select_row, select_col)
                        else:
                            self.highlightbutton(row, col, cir_posx, cir_posy, True)
                            self.setnumber(self.selected_circle[1], self.selected_circle[2])
                        pygame.display.flip()

        if event.type == pygame.KEYDOWN:
            if self._active and self.selected_circle:

                sk = [*self.set_keys.values()]
                csk = [sk.index(k) for k in sk if event.key in k]

                if csk:
                    set_key = int(csk[0]) if event.key != pygame.K_BACKSPACE else 0

                    sr = self.selected_circle[0]
                    select_row = self.selected_circle[1]
                    select_col = self.selected_circle[2]
                    self.highlightbutton(select_row, select_col, sr.x+sr.width/2, sr.y + sr.height/2, True)
                    self.setnumber(select_row, select_col, set_key)
                    self.input_num += [int(str(select_row) + str(select_col))]
        return

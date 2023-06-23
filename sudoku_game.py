
# imports
import pygame
import time
import copy
import sys, os
from utils.sudoku_solver import SudokuBoard

# pygame init
pygame.init()

# set width/height del juego
width, height = 480, 800
surface = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

# global colors
color_white = (255, 255, 255)
safety_base_color = pygame.Color('#66A0BF')
safety_base_inverse = pygame.Color(255-safety_base_color.r, 255-safety_base_color.b, 255-safety_base_color.g)
safety_secondary_color = pygame.Color('#4CC2F0')
safety_secondary_inverse = pygame.Color(255-safety_secondary_color.r, 255-safety_secondary_color.b, 255-safety_secondary_color.g)
hardsolved_circles = pygame.Color('#98b3ed')  


class GameBoard:
    def __init__(self):
        self._active = False
        self.timer = None
        self.count_up = None

        self.board = [[0] * 9 for _ in range(9)]
        self.backbutt_img = pygame.transform.scale(pygame.image.load(resource_path('img/left.png')).convert_alpha(), (30, 30))
        self.restartbutt_img = pygame.transform.scale(pygame.image.load(resource_path('img/restart.png')).convert_alpha(), (36, 36))
        self.donebutt_img = pygame.transform.scale(pygame.image.load(resource_path('img/done.png')).convert_alpha(), (36, 36))
        self.back_button = None

        # fuente basica
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
        # teclas 
        self.set_keys = {0: [pygame.K_0, pygame.K_KP0, pygame.K_DELETE, pygame.K_BACKSPACE],
                         1: [pygame.K_1, pygame.K_KP1], 2: [pygame.K_2, pygame.K_KP2],
                         3: [pygame.K_3, pygame.K_KP3], 4: [pygame.K_4, pygame.K_KP4],
                         5: [pygame.K_5, pygame.K_KP5], 6: [pygame.K_6, pygame.K_KP6],
                         7: [pygame.K_7, pygame.K_KP7], 8: [pygame.K_8, pygame.K_KP8],
                         9: [pygame.K_9, pygame.K_KP9]}

        return

    def oncall(self, diff: str = "beginner"):
        """teclas para que el juego setee la dificultad del tablero y, si no está activo, dibuje el tablero"""
        self.difficulty = diff
        if not self._active:
            self.drawlayout()
        self._active = True
        return self._active

    def drawlayout(self):
        """Esta función para llamar a todos los elementos necesarios para el tablero"""
        self.drawboard()
        self.backbutton()
        theme.themebutton()

    def endgame(self):
        """Función para borrar todas las variables y finalizar el juego actual"""
        self.__init__()
        menu.startgame = False

    def backbutton(self):
        """Dibujar el botón de retroceso en el tablero"""
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
                if row != 9 and col != 9:  # circulos
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
            if i % 3 == 0 and i != 0 and i != 9:  #4 líneas oscuras
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

        self.reset_button = [pygame.draw.circle(surface, safety_secondary_color, (width/4 - 50, height - height/4), 25),
                             pygame.draw.circle(surface, safety_secondary_color, (width/4 + 50, height - height/4), 25),
                             pygame.draw.rect(surface, safety_secondary_color, (width / 4 - 50, height - height / 4 - 25, 100, 50))]

        self.insta_solve_button = [pygame.draw.circle(surface, safety_secondary_color, (width - width/4-50, height - height/4), 25),
                                   pygame.draw.circle(surface, safety_secondary_color, (width - width/4+50, height - height/4), 25),
                                   pygame.draw.rect(surface, safety_secondary_color, (width - width/4-50, height - height/4-25, 100, 50))]

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
        """Dibuje la ventana emergente del menú final del juego con los botones 'ir al menú principal' y 'reproducir'"""
        s = pygame.Surface((480, 800))
        s.set_alpha(50)
        s.fill(safety_base_color)
        surface.blit(s, (0, 0))

        self.popup_menu = [pygame.draw.circle(surface, safety_base_color, (width / 4 - 50, height - height / 4), 24),
                           pygame.draw.circle(surface, safety_base_color, (width / 4 + 50, height - height / 4), 24),
                           pygame.draw.rect(surface, safety_base_color, (width / 4 - 50, height - height / 4 - 24, 100, 48))]

        self.popup_replay = [pygame.draw.circle(surface, safety_base_color, (width - width / 4 - 50, height - height / 4), 24),
                             pygame.draw.circle(surface, safety_base_color, (width - width / 4 + 50, height - height / 4), 24),
                             pygame.draw.rect(surface, safety_base_color, (width - width / 4 - 50, height - height / 4 - 24, 100, 48))]

        pop_menu = self.base_font.render("    Menú", True, safety_secondary_color)
        pop_replay = self.base_font.render("    Nuevo", True, safety_secondary_color)

        surface.blit(pop_menu, (self.popup_menu[-1].x + (self.popup_menu[-1].width / 4 - 33), self.popup_menu[-1].y + (self.popup_menu[-1].height / 4 + 2)))
        surface.blit(pop_replay, (self.popup_replay[-1].x + (self.popup_replay[-1].width / 4 - 31), self.popup_replay[-1].y + (self.popup_replay[-1].height / 4 + 2)))

        if self.insta_solve:
            solv_text = self.base_font.render("Has cometido algún error", True, safety_base_inverse)
            surface.blit(solv_text, (width / 2 - solv_text.get_width() / 2, height - height / 3))
        else:
            won_text = self.base_font.render("¡HAS GANADO!", True, safety_base_inverse)
            surface.blit(won_text, (width / 2 - won_text.get_width() / 2, height - height / 3))
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
        """Función para que los botones de finalización del juego regresen al menú principal o comiencen un nuevo juego"""
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


class ColorTheme:

    def __init__(self):
        self.color = None
        self.theme_logo = pygame.image.load(resource_path('img/theme.png')).convert_alpha()
        self.theme_button = None
        self.bar_position = False
        self.theme_clicked = False
        self.theme_font = pygame.font.Font(None, 32)
        self.themelist = []
        self.theme_colors = {'dark_blue': ("#0D151B", "#4CC2F0"), 'dark_red': ("#1B1B1B", "#FF2470"),
                             'dark_green': ("#151014", "#379534"), 'dark_yellow': ("#181818", "#9C8F5D"),
                             'light_blue': ("#FFFFFF", "#66A0BF"), 'light_red': ("#FFFFFF", "#C16469"),
                             'grey_green': ("#383B35", "#AEC99E")
                             }
        return

    def themebutton(self):
        """This function is for drawing the """
        self.theme_button = pygame.draw.circle(surface, safety_secondary_color, (width-25, 25), 20)
        surlogo = surface.blit(self.theme_logo, self.theme_logo.get_rect(center=self.theme_button.center))
        pygame.display.update([surlogo, self.theme_button])
        return

    def themeselector(self):
        """Function draws possible color combos and displays them in two columns"""
        text_surface = self.theme_font.render("Selecciona un tema", True, (255-safety_base_color.r, 255-safety_base_color.g, 255-safety_base_color.b))
        theme_text = pygame.draw.rect(surface, safety_base_color, (width / 2 - 100, 50, 200, 50))
        surface.blit(text_surface, (theme_text.x + (theme_text.width / 4 - 25), theme_text.y + (theme_text.height / 4)))
        ck = [*self.theme_colors]
        ck_co = 0
        for y in range(1, 6):
            for x in range(1, 3):
                for i in range(25):
                    if ck_co > len(ck) - 1:
                        return
                    time.sleep(0.001)
                    if i == 24:
                        self.themelist += [pygame.draw.circle(surface, self.theme_colors[ck[ck_co]][0], (width * (x / 3), height * (y / 5)), 0 + i)]
                    else:
                        pygame.draw.circle(surface, self.theme_colors[ck[ck_co]][0], (width * (x / 3), height * (y / 5)), 0 + i)
                    if 25 >= i >= 10:
                        pygame.draw.circle(surface, self.theme_colors[ck[ck_co]][1], (width * (x / 3), height * (y / 5)), -10 + i)
                    pygame.display.flip()
                ck_co += 1

    def expandocircle(self, slider_pos=None):
        """Una función para animar el selector de temas en expansión

        :parametro slider_pos: Para cerrar o abrir el selector de temas
        :return:
        """
        if slider_pos is None:
            return
        if slider_pos:  # selector de tema abierto
            for i in range(height):
                if height-i == 50:
                    continue
                circle_pos = (width-25, 25)
                pygame.draw.circle(surface, safety_secondary_color, circle_pos, 20+i+3)
                pygame.draw.circle(surface, safety_base_color, circle_pos, 20+i+1)
                self.themebutton()
                pygame.display.update()
            self.themeselector()

        elif not slider_pos:  # cerrar selector de tema
            for i in range(height):
                if height-i == 20:
                    return False

                if menu.startgame:
                    board.drawlayout()
                else:
                    main_menu()
                circle_pos = (width - 25, 25)
                pygame.draw.circle(surface, safety_secondary_color, circle_pos, 800-i-1)
                pygame.draw.circle(surface, safety_base_color, circle_pos, 800-i-3)
                self.themebutton()
                pygame.display.update()
        return

    def themeevent(self, event) -> bool:
        """Función para cambiar entre los diferentes temas al presionar el mouse

        :return: Booleano si el selector de tema está abierto
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.theme_button.collidepoint(event.pos) and not self.bar_position:
                self.expandocircle(True)
                self.bar_position = True
            elif self.theme_button.collidepoint(event.pos) and self.bar_position:
                self.expandocircle(False)
                self.bar_position = False

            if self.bar_position:
                for i, bg in enumerate(self.themelist):
                    if bg.collidepoint(event.pos) and self.bar_position:
                        global safety_base_color, safety_secondary_color, safety_base_inverse, safety_secondary_inverse

                        safety_base_color = pygame.Color(list(self.theme_colors.values())[i][0])
                        safety_secondary_color = pygame.Color(list(self.theme_colors.values())[i][1])
                        safety_base_inverse = pygame.Color(255-safety_base_color.r, 255-safety_base_color.b, 255-safety_base_color.g)
                        safety_secondary_inverse = pygame.Color(255-safety_secondary_color.r, 255-safety_secondary_color.b, 255-safety_secondary_color.g)

                        self.expandocircle(True)
                        break

        return self.bar_position


class MainMenu:
    def __init__(self):
        self.newgame_button = []
        self.startgame = False
        self.left_arr = None
        self.right_arr = None
        self.render_diff = None
        self.base_font = pygame.font.Font(None, 32)
        self.diff_txt = pygame.font.Font(None, 24)
        self.logo = pygame.image.load(resource_path('img/main_logo.png')).convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (700, 700))
        self.logo = pygame.transform.rotate(self.logo, 0)

        self.difficulty = ['Principiante', 'Fácil', 'Medio', 'Difícil', 'Extremo']
        self.diff_iter = 0

    def diff(self):
        return self.difficulty[self.diff_iter]

    def fade(self, w, h, slide, side):
        """Función para animar el desplazamiento horizontal del selector de dificultad cuando se presiona la flecha"""
        fade = pygame.Surface((w, h))
        fade.fill(safety_base_color)

        if side == "derecha":
            if slide < 0:
                fade.set_alpha(abs(slide)*4)
            elif slide >= 0:
                fade.set_alpha(slide)
        elif side == "izquierda":
            if slide < 0:
                fade.set_alpha(255-slide*2)
            elif slide >= 0:
                fade.set_alpha(slide*4)

        surface.blit(fade, (width/3+41+slide, height/2+30, 75, 25))
        pygame.display.flip()
        pygame.time.delay(5)

    def draw_static_menu(self):
        """Función para cargar el menú principal"""

        surface.fill(safety_base_color)

        cir = pygame.draw.circle(surface, safety_secondary_color, (width/2, height/3), 75)
        surface.blit(self.logo, self.logo.get_rect(center=cir.center))

        text_surface = self.base_font.render("Juego Nuevo", True, safety_base_color)

        self.left_arr = pygame.draw.lines(surface, safety_base_inverse, False, [(width/4, height/2+50), (width/4-8, height/2+50-8), (width/4, height/2+50-16)], 5)
        self.right_arr = pygame.draw.lines(surface, safety_base_inverse, False, [(width-(width/4), height/2+50), (width-(width/4)+8, (height/2)+50-8), (width-(width/4), (height/2)+50-16)], 5)

        self.newgame_button = [pygame.draw.circle(surface, safety_secondary_color, (width/4, height/2+100), 25),
                               pygame.draw.circle(surface, safety_secondary_color, (width-(width/4), height / 2 + 100), 25),
                               pygame.draw.rect(surface, safety_secondary_color, (width/4, height/2+100-25, 245, 50))]

        surface.blit(text_surface, (self.newgame_button[-1].x + (self.newgame_button[-1].width/4+5), self.newgame_button[-1].y + (self.newgame_button[-1].height/4+2)))
        return

    def draw_dynamic_menu(self, i=0):
        """Dibujar cuadro de animación de dificultad de desplazamiento"""
        pygame.draw.rect(surface, safety_base_color, (width/3+41+i, height/2+30, 75, 25))
        self.render_diff = self.diff_txt.render(self.difficulty[self.diff_iter], True, safety_base_inverse)
        txwid = self.render_diff.get_width()
        surface.blit(self.render_diff, ((width/2)-(txwid/2)+i, height*2/4+36))
        return

    def mouse_press(self, event):
        """Función para detectar la presión del mouse para la animación de desplazamiento de dificultad del menú principal"""
        event.pos = (0, 0) if not hasattr(event, 'pos') else event.pos
        event.key = 0 if not hasattr(event, 'key') else event.key

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            if self.left_arr.collidepoint(event.pos) or event.key == pygame.K_LEFT:
                # mover el selector de dificultad a la izquierda
                for slide in range(80):
                    self.draw_dynamic_menu(slide)
                    if slide >= 50:
                        self.fade(75, 25, slide, "izquierda")
                if self.diff_iter != 0:
                    self.diff_iter -= 1
                for slide in reversed(range(80)):
                    self.draw_dynamic_menu(-slide)
                    if slide <= 20:
                        self.fade(75, 25, -slide, "izquierda")

            elif self.right_arr.collidepoint(event.pos) or event.key == pygame.K_RIGHT:
                # mover el selector de dificultad a la derecha
                for slide in range(80):
                    self.draw_dynamic_menu(-slide)
                    if slide >= 50:
                        self.fade(75, 25, -slide, "derecha")
                if self.diff_iter != len(self.difficulty) - 1:
                    self.diff_iter += 1
                for slide in reversed(range(80)):
                    self.draw_dynamic_menu(slide)
                    if slide <= 20:
                        self.fade(75, 25, slide, "derecha")
            pygame.display.flip()

    def startplaying(self, event):
        """Función para iniciar el juego si se presiona el botón de nuevo juego"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            newgame_button = [x for x in self.newgame_button if x.collidepoint(event.pos)]

            if not self.startgame and newgame_button:
                self.startgame = True
                return self.startgame
        return False


def cleanup(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()


def main_menu():
    """Función para dibujar menú y botón de tema a la vez"""
    menu.draw_static_menu()
    menu.draw_dynamic_menu()
    theme.themebutton()


def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrolladores y para PyInstaller"""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    global board, menu, theme
    board = GameBoard()
    menu = MainMenu()
    theme = ColorTheme()
    main_menu()
    pygame.display.flip()
    difficulty = "Principiante"
    theme_stat = False
    set_scene = -1  # 0 menu, 1 board, 2 end popup
    current_scene = 0

    while True:
        if set_scene == 0:  # menu
            main_menu()
            pygame.display.flip()
        elif set_scene == 1:  # board
            board.oncall(difficulty)
            pygame.display.flip()
        elif set_scene == 2:  # popup
            board.end_game_popup()
        set_scene = -1
        for event in pygame.event.get():
            cleanup(event)
            if current_scene != 2:
                # comprobando si el selector de tema está activo
                theme_stat = theme.themeevent(event)

            if current_scene == 1 and board.solved():
                # comprobar si el tablero está resuelto
                set_scene = current_scene = 2
                continue

            if current_scene == 0 and not theme_stat:
                # main menu
                menu.mouse_press(event)
                if menu.startplaying(event):
                    # start game
                    difficulty = menu.diff()
                    set_scene = current_scene = 1
            elif current_scene == 1 and not theme_stat:
                board.onkeypress(event)
                if not board.backbutton_event(event):
                    set_scene = current_scene = 0

            if current_scene == 2:
                pop_action = board.end_game_popup_action(event)
                if pop_action is None:
                    continue
                elif pop_action:
                    set_scene = -1  # esto está seteado en -1, por lo que no dibuja dos veces el tablero
                    current_scene = 1  # se setea en 1 porque permite que los botones del tablero se activen
                else:
                    set_scene = current_scene = 0



if __name__ == "__main__":
    main()

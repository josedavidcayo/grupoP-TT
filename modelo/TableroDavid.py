class Tablero:
    def __init__(self):
        self.tablero = [[0] * 9 for _ in range(9)]
        self.generarTablero()

    def generarTablero(self):
        self.llenarTodasLasCajas()
        self.eliminarElementos(20)

    def llenarTodasLasCajas(self):
        flag = [False for _ in range(9)]
        vacia = self.encontrarVacia()

        if vacia is None:
            return True

        fila, columna = vacia[0], vacia[1]
        while True:
            num = randint(1, 9)
            flag[num - 1] = True
            if self.esSeguroInsertar(fila, columna, num):
                self.tablero[fila][columna] = num
                if self.llenarTodasLasCajas():
                    return True
                self.tablero[fila][columna] = 0

            if flag.count(True) == 9:
                return False


    def resolver(self):
        vacia = self.encontrarVacia()

        if vacia is None:
            return True

        fila, columna = vacia[0], vacia[1]

        for num in range(1, 10):
            if self.esSeguroInsertar(fila, columna, num):
                self.tablero[fila][columna] = num
                if self.resolver():
                    return True
                self.tablero[fila][columna] = 0
        return False

    def esFilaSegura(self, fila, num):
        for i in range(9):
            if self.tablero[fila][i] == num:
                return False
        return True

    def esColumnaSegura(self, columna, num):
        for i in range(9):
            if self.tablero[i][columna] == num:
                return False
        return True

    def esCajaInternaSegura(self, fila, columna, num):
        for i in range(3):
            for j in range(3):
                if self.tablero[fila + i][columna + j] == num:
                    return False
        return True

    def esSeguroInsertar(self, fila, columna, num):
        return (
            self.esFilaSegura(fila, num)
            and self.esColumnaSegura(columna, num)
            and self.esCajaInternaSegura(fila - fila % 3, columna - columna % 3, num)
        )

    def eliminarElementos(self, count):
        while count != 0:
            index = randint(0, 80)
            fila, columna = int(index / 9), index % 9
            while self.tablero[fila][columna - 1 if columna != 0 else columna] == 0:
                index = randint(0, 80)
                fila, columna = int(index / 9), index % 9 - 1
            self.tablero[fila][columna - 1 if columna != 0 else columna] = 0
            count -= 1

    def encontrarVacia(self):
        for i in range(9):
            for j in range(9):
                if self.tablero[i][j] == 0:
                    return [i, j]
        return None
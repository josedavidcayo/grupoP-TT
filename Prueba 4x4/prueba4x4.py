import random

def generar_sudoku():
    # Crea una matriz vacía de 4x4
    
    sudoku = [[0] * 4 for _ in range(4)]

    # Rellena la matriz con números aleatorios del 1 al 4
    numeros = [1, 2, 3, 4]
    
    random.shuffle(numeros)

    for i in range(4):
        for j in range(4):
            
            sudoku[i][j] = numeros[(i + j) % 4]

    return sudoku

def imprimir_sudoku(sudoku):
    
    for i in range(4):
        for j in range(4):
            
            if sudoku[i][j] == 0:
                print("-", end=" ")
            else:
                print(sudoku[i][j], end=" ")
        print()

def resolver_sudoku(sudoku):
    
    for i in range(4):
        for j in range(4):
            
            if sudoku[i][j] == 0:
                for num in range(1, 5):
                    
                    if validar_movimiento(sudoku, i, j, num):
                        sudoku[i][j] = num
                        if resolver_sudoku(sudoku):
                            return True
                        sudoku[i][j] = 0
                return False
    return True

def validar_movimiento(sudoku, fila, columna, numero):
    # Verificar la fila
    for j in range(4):
        
        if sudoku[fila][j] == numero:
            return False

    # Verificar la columna
    for i in range(4):
        
        if sudoku[i][columna] == numero:
            return False

    return True

# Genera un sudoku
sudoku = generar_sudoku()

# Determina la cantidad de celdas vacías
num_celdas_vacias = random.randint(7, 10)

# Vacía algunas celdas del sudoku
for _ in range(num_celdas_vacias):
    
    fila = random.randint(0, 3)
    columna = random.randint(0, 3)
    sudoku[fila][columna] = 0

# Imprime el sudoku inicial
print("Sudoku inicial:")
imprimir_sudoku(sudoku)
print()

# Resuelve el sudoku automáticamente
#resolver_sudoku(sudoku)

# Imprime el sudoku resuelto
print("Sudoku a resolver:")
imprimir_sudoku(sudoku)
print()

# Permite al usuario completar las celdas vacías
print("Complete las celdas vacías:")
for i in range(4):
    for j in range(4):
        
        if sudoku[i][j] == 0:
            valido = False
            while not valido:
                
                valor = input(f"Ingrese el número para la posición [{i+1}][{j+1}]: ")
                if valor.isdigit() and 1 <= int(valor) <= 4:
                    
                    valor = int(valor)
                    if validar_movimiento(sudoku, i, j, valor):
                        sudoku[i][j] = valor
                        valido = True
                    else:
                        print("El número ingresado no es válido. Inténtelo nuevamente.")
                else:
                    print("Ingrese un número válido (1-4). Inténtelo nuevamente.")

# Imprime el sudoku con los valores ingresados por el usuario

print("Sudoku final:")

imprimir_sudoku(sudoku)
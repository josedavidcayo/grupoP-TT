class Celda():
    def __init__(self):
        self.valor=" "
    
    #rellena la celda
    def set_celda(self,dato):
        self.valor=dato
        
    #vacia la celda
    def borrar_celda(self):
        self.valor=" "
        
    def get_celda(self):
        return self.valor
        
class Tablero:
    def __init__(self):
        self.tablero=[[Celda() for x in range(9)] for y in range(9)]
        
    def get_tablero(self):
        return self.tablero




#funcion para ver el tablero y el valor de cada celda

def ver_tablero(): 
    for x in range(9):
        for y in range(9):
            print(tablero.get_tablero()[x][y].get_celda(),end="|")
        print("\n")
        
    return ""

#settea un numero del tablero

def ingresa_dato():
    error_dato=False
    try:
        dato=int(input("Numero a ingresar: "))
        comprueba(dato)
        if error_dato:
            print("Debes ingresar un numero entre 1 y 9")
        fila=int(input("En que fila ?: "))
        comprueba(fila)
        if error_dato:
            print("Debes ingresar un numero entre 1 y 9")
        columna=int(input("Y en que columna?: "))
        comprueba(columna)
        if error_dato:
            print("Debes ingresar un numero entre 1 y 9")
    except Exception:
        print("Debes ingresar un numero...")

    print("\n")
    
    tablero.get_tablero()[fila-1][columna-1].set_celda(dato)

#borra un dato del tablero
def borrar_dato():
    error_dato=False
    
    try:
        fila=int(input("En que fila esta el dato que quieres borrar?: "))
        comprueba(fila)
        if error_dato:
            print("Debes ingresar un numero entre 1 y 9")
        columna=int(input("Y en que columna?: "))
        comprueba(columna)
        if error_dato:
            print("Debes ingresar un numero entre 1 y 9")
    except Exception:
        print("Debes ingresar un numero...")

    print("\n")
    
    tablero.get_tablero()[fila-1][columna-1].borrar_celda()

#Revisa que los datos ingresados sean correctos
def comprueba(dato):
    if dato<1 or dato>9:
        return False
    return True

#Metodo main

tablero=Tablero()

while True:
    print(ver_tablero()+"\n")
    try:
        opcion=int(input("Que desea hacer?\n1)Llenar celda\n2)Borrar Celda\n"))
        if opcion==1:
            ingresa_dato()
        if opcion==2:
            borrar_dato()
        else:
            print("Ingrese una opcion valida, por favor.")    
    except Exception:
        print("Debe escribir un numero...")

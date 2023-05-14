import os
import copy

# Opciones que tiene el menú del sudoku
MENU = ["  a - Fijar valor de una celda. ", 
	"  b - Borrar valor de una celda", 
	"  c - Agregar opción a una celda.",
    "  d - Borrar opción de una celda.",
    "  e - Verificar factible.",
    "  f - Deshacer.",
    "  g - Mostrar opciones de una celda.",
    "  h - Salir.",""]

def Entrada(devolver_valor=True):
	"""Función que facilita la lectura de los parámetros fila, columna y
	 valor (este último opcional) desde el teclado."""
	fila=columna=valor=0
	while fila<1 or fila>9:
		try: fila = int(input
			("Introduce el número de fila (entre 1 y 9): "))
		except Exception: print("Valor no valido.")
	while columna<1 or columna>9:
		try: columna = int(input
			("Introduce el número de columna (entre 1 y 9): "))
		except Exception: print("Valor no valido.")
	while devolver_valor and valor<1 or valor>9:
		try: valor = int(input
		("Introduce el valor (entre 1 y 9): "))
		except Exception: print("Valor no valido.")
	if devolver_valor: return fila, columna, valor
	else: return fila, columna

class Celda():
	"""Una celda contiene un valor y un conjunto de opciones de valores 
	para esta celda. Una celda vacía se representa como una celda cuyo 
	valor es cero. Una celda puede ser fija, es decir, su valor no puede
	 ser modificado una vez que es introducido. El invariante de la 
	 clase celda especifica que si una celda no está vacía entonces 
	 el conjunto de opciones debe estar vacío."""
	def __init__(self):
		self.__valor = 0
		self.__fija = False
		self.__opciones = []
		
	def fijar_valor(self, dato, fija = False):
		"""Método para introducir un valor en una celda e indicar si 
		el mismo es o no fijo. Si la celda ya es fija entonces no se 
		puede modificar y por tanto devuelve False. En caso contrario 
		devuelve True."""
		if not self.__fija:
			self.__valor = dato
			self.__fija = fija
			self.__opciones = []
			return True
		return False
		
	def borrar_valor(self):
		"""Método que borra el contenido de una celda."""
		if not self.__fija:
			self.__valor = 0
			return True
		return False
	
	def valor(self):
		"""Método que devuelve el valor que aloja la celda."""
		return self.__valor
		
	def valida(self):
		"""Método que devuelve True si la celda no está vacía y 
		False en caso contrario."""
		if self.__valor == 0:
			return False
		return True
	
	def fija(self):
		"""Método que devuelve True si la celda es fija y False 
		en caso contrario."""
		return self.__fija
	
	def nueva_opcion(self, dato):
		"""Método que guarda una nueva opción en la celda. Si el dato ya
		existe en el conjunto de posibles opciones, entonces devuelve 
		False sino devuelve True."""
		if not self.__fija and dato not in self.__opciones:
			self.__opciones.append(dato)
			return True 
		return False
	
	def borrar_opcion(self, dato):
		"""Método que borra una opción de la celda. Si el dato no existe
		 en el conjunto de posibles opciones, entonces devuelve False 
		 sino devuelve True.""" 
		if not self.__fija and dato in self.__opciones:
			self.__opciones.remove(dato)
			return True
		return False
	
	def opciones(self):
		"""Método que devuelve las opciones de la celda.""" 
		self.__opciones.sort()
		return self.__opciones
	
	def __str__(self):
		"""Método llamado para crear una cadena de texto que represente
		el valor definitivo de la celda en caso de que sea válido, sino 
		mostará un "_"."""
		return str(self.__valor) if self.__valor else "_" 

class Sudoku():
	"""Un sudoku contiene un tablero de celdas de tamaño 9*9 y una pila
	 de jugadas. El tablero puede tener tanto celdas fijas como 
	 modificables. El invariante de la clase especifica que cada celda 
	 del tablero y cada elemento de la lista de opciones de la celda 
	 debe tener valores entre 0 y 9 en donde el cero representa una 
	 celda vacía. Además no puede haber en una misma fila, columna o 
	 bloque dos valores iguales, ni en la celda ni en la lista de 
	 opciones de la misma."""
	def __init__(self):
		self.__tablero = [[Celda() for x in range(9)] for y in range(9)]
		self.__jugadas = []
		try:
			os.system("python generador.py > tablero.txt")
			f = open("tablero.txt", "r")
		except:
			print ("Error: Imposible cargar tablero de juego")
			SystemExit.exit(1)
		f.readline()
		fila = 0
		while fila < 9:
			linea = f.readline().split()
			if linea != []:
				for i in range(9):
					if linea[i] != "_":
						self.__tablero[fila][i].fijar_valor\
						(int(linea[i]),True)
				fila+= 1
		try: os.system("rm -f tablero.txt")
		finally: f.close()
	
	def fijar_valor(self, fila, columna, valor):
		"""Método que fija el valor dado en la celda ubicada en la
		 posición (fila,columna) del tablero. En caso de que la jugada
		  sea valida, en cuyo caso se devolverá True, o False en caso 
		  contrario."""
		if self.es_factible(fila, columna, valor):
			jugada = []
			jugada.append((fila-1, columna-1,copy.deepcopy\
			(self.__tablero[fila-1][columna-1])))
			for i in range(9):
				if i!= columna-1 and valor in\
				 self.__tablero[fila-1][i].opciones():
					jugada.append((fila-1, i,copy.deepcopy\
					(self.__tablero[fila-1][i])))
					self.__tablero[fila-1][i].borrar_opcion(valor)
				if i!= fila-1 and valor in\
				 self.__tablero[i][columna-1].opciones():
					jugada.append((i, columna-1,copy.deepcopy\
					(self.__tablero[i][columna-1])))
					self.__tablero[i][columna-1].borrar_opcion(valor)
			f = 3 * ((fila-1)/3)
			c = 3 * ((columna-1)/3)
			for i in range(f,f+3):
				for j in range(c,c+3):
					if i!= fila-1 and j!= columna-1 and valor in\
					 self.__tablero[i][j].opciones():
						jugada.append((i, j,copy.deepcopy\
						(self.__tablero[i][j])))
						self.__tablero[i][j].borrar_opcion(valor)
			self.__jugadas.append(jugada)
			return self.__tablero[fila-1][columna-1].fijar_valor(valor)
		return False
		
	def borrar_valor(self, fila, columna):
		"""Método que elimina el valor de la celda ubicada en la 
		posición (fila,columna) del tablero."""
		if 0 < fila < 10 and 0 < columna < 10 and\
		self.__tablero[fila-1][columna-1].valida() and\
		not self.__tablero[fila-1][columna-1].fija():
			self.__jugadas.append([(fila-1, columna-1,copy.deepcopy\
			(self.__tablero[fila-1][columna-1]))])
			return self.__tablero[fila-1][columna-1].borrar_valor()
		return False
		
	def finalizado(self):
		"""Método que devuelve True si el juego ha finalizado,
		 es decir, todas las celdas contienen valores y éstos son 
		 válidos según las reglas del juego."""
		for i in range(9):
			for j in range(9):
				if not self.__tablero[i][j].valida():
					return False
		return True
	
	def opciones(self, fila, columna):
		"""Método que devuelve las opciones que ha dejado el jugador
		 guardadas en la celda ubicada en la posición (fila,columna) 
		 del tablero."""
		if 0 < fila < 10 and 0 < columna < 10:
			return self.__tablero[fila-1][columna-1].opciones()
	
	def nueva_opcion(self, fila, columna, valor):
		"""Método que guarda un nuevo valor en las opciones de la celda
		 ubicada en la posición (fila,columna) del tablero. Si el dato 
		 ya existe en las opciones de la celda, entonces devuelve False 
		 sino devuelve True."""
		if not self.__tablero[fila-1][columna-1].valida() and\
		self.es_factible(fila, columna, valor) and valor not in\
		 self.__tablero[fila-1][columna-1].opciones():
			self.__jugadas.append([(fila-1, columna-1,copy.deepcopy\
			(self.__tablero[fila-1][columna-1]))])
			return self.__tablero[fila-1][columna-1].nueva_opcion(valor)
		return False		
			
	def borrar_opcion(self, fila, columna, valor):
		"""Método que borra el valor indicado de las opciones de la 
		celda ubicada en la posición (fila,columna) del tablero. Si el 
		dato no existe en las opciones de la celda, entonces devuelve 
		False sino devuelve True."""
		if 0 < fila < 10 and 0 < columna < 10 and valor in\
		 self.__tablero[fila-1][columna-1].opciones():
			self.__jugadas.append([(fila-1, columna-1,copy.deepcopy\
			(self.__tablero[fila-1][columna-1]))])
			return self.__tablero[fila-1][columna-1].borrar_opcion\
			(valor) 
		return False
	
	def es_factible(self, fila, columna, valor):
		"""Método que devuelve True si el valor dado puede ubicarse en 
		la celda ubicada en la posición (fila,columna) del tablero según
		las reglas del juego."""
		if 0 < fila < 10 and 0 < columna < 10 and 0 < valor < 10 and\
		not self.__tablero[fila-1][columna-1].fija():
			for i in range(9):
				if self.__tablero[fila-1][i].valor() == valor or\
				self.__tablero[i][columna-1].valor() == valor:
					return False
			f = 3 * ((fila-1)/3)
			c = 3 * ((columna-1)/3)
			for i in range(f,f+3):
				for j in range(c,c+3):
					if i!= fila-1 and j!= columna -1 and\
					self.__tablero[i][j].valor() == valor:
						return False
			return True
		return False
	
	def undo(self):
		"""Método que deshace la ultima jugada. En el caso en que no 
		haya más jugadas para deshacer la función devuelve False sino 
		devuelve True."""
		if self.__jugadas != []:
			jugada = self.__jugadas.pop()
			for jugadas in jugada:
				self.__tablero[jugadas[0]][jugadas[1]] = jugadas[2]
			return True
		return False
				  
	def __str__(self):
		"""Método llamado para crear una cadena de texto que represente
	el tablero del sudoku."""
		sudoku = 10*" "+ "Tablero" + 10* " "+"Opciones\n"
		for i in range(9):
			linea = str(i+1)
			for j in range(9):
				if j%3 == 0:
					linea+= " " 
				linea+= "|"+str(self.__tablero[i][j])
				if j==2 or j==5 or j==8:
					linea+="|"
			linea+=MENU[i]
			if((i+1)%3 == 0):
				linea+="\n"
			linea+="\n"
			sudoku+=linea
			linea = str(i+1)
		sudoku+= "   1 2 3   4 5 6   7 8 9\n"
		return sudoku

def main(): 
	sudoku = Sudoku()
	opcion = ""
	os.system("clear")
	mensaje = "Sudoku en Python: \n"
 
	while(not sudoku.finalizado() and opcion!= "h"):
		print (mensaje)
		print (sudoku)
		opcion=input("\nIntroduce una opción: ")
		if(opcion=="a"):
			fila, columna , valor = Entrada()
			if sudoku.fijar_valor(fila, columna, valor):
				mensaje = "Valor de la celda ("+ str(fila) + ","\
				+ str(columna) + ") fijado correctamente."
			else: mensaje = "Imposible fijar valor. Revise la jugada."
		elif opcion =="b":
			fila, columna = Entrada(False)
			if sudoku.borrar_valor(fila,columna):
				mensaje = "Valor de la celda ("+ str(fila) + ","\
				+ str(columna) + ") borrado correctamente."
			else: mensaje = "Imposible borrar valor. Revise la jugada."
		elif opcion == "c":
			fila, columna, valor = Entrada()
			if sudoku.nueva_opcion(fila,columna, valor):
				mensaje = "Opción de la celda ("+ str(fila) + ","\
				+ str(columna) + ") agregada correctamente."
			else: mensaje = "Imposible agregar opción. Revise la jugada."
		elif opcion == "d":
			fila, columna, valor = Entrada()
			if sudoku.borrar_opcion(fila, columna, valor):
				mensaje = "Opción de la celda ("+ str(fila) + ","\
				+ str(columna) + ") borrada correctamente."
			else: mensaje = "Imposible borrar opción. Revise la jugada."
		elif opcion == "e":
			fila, columna, valor = Entrada()
			if sudoku.es_factible(fila,columna,valor):
				mensaje = "SI es factible introducir el valor "\
				+ str(valor) +" en la celda ("+ str(fila) + ","\
				+ str(columna) +")."
			else: mensaje = "NO es factible introducir el valor "\
				+ str(valor) + " en la celda ("+ str(fila) + ","\
				+ str(columna) + ")."
		elif opcion == "f":
			if sudoku.undo(): mensaje ="Jugada deshecha."
			else: mensaje = "Imposible deshacer la jugada."
		elif opcion == "g":
			fila, columna = Entrada(False)
			if sudoku.opciones(fila,columna) != []:
				mensaje ="La celda (" + str(fila) + ","\
				+ str(columna) + ") tiene como opciones: "\
				+ str(sudoku.opciones(fila,columna))
			else: mensaje="La celda (" + str(fila) + ","\
				+ str(columna) + ") no tiene ninguna opción."
		else: mensaje = "Introduzca una opción correcta."
		os.system("clear")
	if opcion == "h": print ("¡Adiós!")
	else: print ("Sudoku completado. Enhorabuena.")
	return 0

main()
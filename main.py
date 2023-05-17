from modelo.JugadorDAO import JugadorDAO
from modelo.Jugador import Jugador

jugadorDAO = JugadorDAO()

print ("--------------------------------")
print ("Listar todos los jugadores. ")
print ("--------------------------------")
jugadores = jugadorDAO.listarJugadores()
for jugador in jugadores:
    print( str(jugador.getId()) + " " +jugador.getNickName() +" ha jugado "+ str(jugador.getPlayedTime()))
    
print ("--------------------------------")
print ("Jugador por id 1")
print ("--------------------------------")
print (jugadorDAO.getJugadorById(1).getNickName())

print ("--------------------------------")
print ("Jugador por nickname")
print ("--------------------------------")
print (jugadorDAO.getJugadorByNickName("Maurinho").getId())


jugador1 = jugadorDAO.getJugadorById(5)

print( jugador1.getNickName() ) #Me da error esta instruccion

#Abra que crear clases para cada tipo de sudoku? y para cada difultad?
#Soy el agustin, perdon que pregunte boludeces pero todavia estoy aprendiendo python :facepalm:


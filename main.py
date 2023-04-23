from modelo.JugadorDAO import JugadorDAO
from modelo.Jugador import Jugador

player = Jugador()

player.setNickName("David_AA")
player.setPlayedTime( 15 )
player.setScore( 0 )
player.setDifficulty( 1)

jugadorDAO = JugadorDAO()
jugadorDAO.crearTablaJugadores()
jugadorDAO.setJugador( player )

jugadorDAO.addJugador()

jugador1 = jugadorDAO.getJugadorById(0)

print( jugador1.getNickName() ) #Me da error esta instruccion

#Abra que crear clases para cada tipo de sudoku? y para cada difultad?
#Soy el agustin, perdon que pregunte boludeces pero todavia estoy aprendiendo python :facepalm:
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

print( jugador1.getNickName() )
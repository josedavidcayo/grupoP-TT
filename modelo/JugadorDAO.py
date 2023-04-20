from db.ConexionDB import ConexionDB
from modelo.Jugador import Jugador

class JugadorDAO:
    def __init__(self):
        self._conexion = ConexionDB('./db/sudokuMDI.db')
        self.con = self._conexion.getConexion()
        self.cursor = self.con.cursor()
        self.crearTablaJugadores()  #Creamos tabla en caso de que no exista.

        self.jugador = None


    def crearTablaJugadores(self):
        cursor = self.con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickName TEXT NOT NULL,
                playedTime INTEGER NOT NULL,
                score INTEGER NULL,
                difficulty INTEGER NULL
            );
        """)
        self.con.commit()       

    def addJugador(self):
        cursor = self.con.cursor()
        cursor.execute("""
            INSERT INTO jugadores (nickName, playedTime, score, difficulty)
            VALUES (?,?,?,?)
        """, (self.jugador.getNickName(), self.jugador.getPlayedTime(), self.jugador.getScore(), self.jugador.getDifficulty()))
        self.con.commit()
    
    def getJugadorById(self, id):
        cursor = self.con.cursor()
        cursor.execute("""
            SELECT * FROM jugadores
            WHERE id =?
        """, (id,))
        for row in cursor:
            self.jugador = Jugador()
            self.jugador.setId(row[0])
            self.jugador.setNickName(row[1])
            self.jugador.setPlayedTime(row[2])
            self.jugador.setScore(row[3])
            self.jugador.setDifficulty(row[4])
            return self.jugador
        
    
    def updateJugador(self):
        cursor = self.con.cursor()
        cursor.execute("""
            UPDATE jugadores
            SET nickName =?, playedTime =?, score =?, difficulty =?
            WHERE id =?
        """, (self.jugador.getNickName(), self.jugador.getPlayedTime(), self.jugador.getScore(), self.jugador.getDifficulty(), self.jugador.getId()))
        self.con.commit()
    
    def deleteJugador(self, id):
        cursor = self.con.cursor()
        cursor.execute("""
            DELETE FROM jugadores
            WHERE id =?
        """, ( id ))
        self.con.commit()

    def listarJugadores(self):
        cursor = self.con.cursor()
        jugadores = []
        cursor.execute("""
            SELECT * FROM jugadores
        """)
        for row in cursor:
            jugador = Jugador()
            jugador.setId(row[0])
            jugador.setNickName(row[1])
            jugador.setPlayedTime(row[2])
            jugador.setScore(row[3])
            jugador.setDifficulty(row[4])
            jugadores.append(jugador)
        return jugadores

    def setJugador(self, jugador):
        self.jugador = jugador

    def getJugadorByNickName(self, nickname):
        cursor = self.con.cursor()
        cursor.execute("""
            SELECT * FROM jugadores
            WHERE  nickName=?
        """, (nickname,))
        
        fila = cursor.fetchone()

        if fila is None:
            print("No se encontro el jugador: " + nickname)
        else:
            self.jugador = Jugador()
            self.jugador.setId(fila[0])
            self.jugador.setNickName(fila[1])
            self.jugador.setPlayedTime(fila[2])
            self.jugador.setScore(fila[3])
            self.jugador.setDifficulty(fila[4])
            return self.jugador
            

# Cerrar la conexión
    def cerrarConexion(self):
        self.conexion.cerrarConexion()
    
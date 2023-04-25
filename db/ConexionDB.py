import sqlite3

class ConexionDB:

    def __init__(self, dbNombre):
        self.dbNombre = dbNombre
        self.conexion = None

    def getConexion(self):
        if not self.conexion:
            self.conexion = sqlite3.connect(self.dbNombre)
        return self.conexion

    def cerrarConexion(self):
        if self.conexion:
            self.conexion.close()
            self.conexion = None
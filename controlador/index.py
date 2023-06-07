from flask import render_template, jsonify
from modelo.Tablero import Tablero



tablero = Tablero(1)

def index():
    return render_template('index.html')


def nuevoTablero():
    tablero.vaciarTablero()
    tablero.generarTablero()

    return jsonify(tabAJugar=tablero.getTablero())

def tablerosRandom():
    return '1 , 2 , 3'

from flask import render_template, jsonify
from modelo.Tablero import Tablero



tablero = Tablero(1)
tabAJugar = tablero.getTablero()

def index():
    return render_template('index.html')


def nuevoTablero():
    return jsonify(tabAJugar=tabAJugar)

def tablerosRandom():
    return '1 , 2 , 3'

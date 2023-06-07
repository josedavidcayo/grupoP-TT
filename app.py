from flask import Flask, render_template
from controlador.index import index, nuevoTablero, tablerosRandom

app = Flask( __name__ )



#Rutas para consumir.
@app.route('/')
def home():
    return index()
    
@app.route('/nuevo')
def nuevo():
    return nuevoTablero()

@app.route('/tableros')
def tableros():
    return tablerosRandom()



if __name__ == "__main__":
    app.run(debug=True)


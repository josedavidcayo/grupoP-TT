#!/bin/bash

# Verifica si python3.11 está instalado
if command -v python3.11 &>/dev/null; then
    echo "Python 3.11 esta instalado."
else
# Añadimos los repositorios PPA de deadsnake para la ultima version de python3
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update
    echo "Repo PPA anñadido"

    sudo apt-get install -y python3.11 python3.11-distutils curl 

    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

    python3.11 -m pip --version
fi

if python3.11 -m pip --version >/dev/null 2>&1; then
    echo "El módulo pip está instalado para Python 3.11."
else
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
    python3.11 -m pip --version
fi

python3.11 -m pip install pygame

python3.11 sudoku_game.py


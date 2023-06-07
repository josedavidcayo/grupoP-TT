console.log("hola");

//generamos el tablero
var tablero = generarTablero();
var boardContainer = document.getElementById("sudoku-board");

//despues meteriamos una variable para el tamaño del sudoku
for (var r = 0; r < 9; r++) {
  for (var c = 0; c < 9; c++) {
    var cell = document.createElement("div");
    cell.classList.add("sudoku-cell");
    cell.textContent = tablero[r][c];
    boardContainer.appendChild(cell);
    //Ver como lo puedo cambiar para que se adapte a los tableros mas grandes
    if (r == 2 || r == 5) {
      cell.classList.add("vertical-line");
    }
    if (c == 2 || c == 5) {
      cell.classList.add("horizontal-line");
    }
    if (cell.textContent != "") {
      cell.classList.add("tile-start");
    }
  }
}

function generarTablero() {
  var tablero1 = [
    [4, null, null, null, null, 1, null, null, null],
    [null, 5, 8, null, null, null, 6, null, 3],
    [null, null, null, null, 6, null, null, 8, 4],
    [null, null, null, 9, 1, null, 5, null, null],
    [6, 8, null, 4, 7, null, 1, 3, 2],
    [5, 7, 1, 6, 2, null, null, 9, 8],
    [8, 9, null, null, 5, 2, null, null, null],
    [null, null, null, null, 8, null, 3, null, null],
    [null, 1, 4, null, null, 6, null, 2, null],
  ];

  return tablero1;
}

window.addEventListener("DOMContentLoaded", function () {
  var timerElement = document.getElementById("timer");
  var seconds = 0;
  var minutes = 0;
  var hours = 0;

  function updateTimer() {
    seconds++;
    if (seconds === 60) {
      seconds = 0;
      minutes++;
      if (minutes === 60) {
        minutes = 0;
        hours++;
      }
    }

    var timeString = pad(hours) + ":" + pad(minutes) + ":" + pad(seconds);
    timerElement.textContent = timeString;
  }

  function pad(num) {
    return (num < 10 ? "0" : "") + num;
  }

  setInterval(updateTimer, 1000);
});
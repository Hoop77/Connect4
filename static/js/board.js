/**
 * Game logic utils
 */

function checkWinner() {
	// check horizontal spaces
	for (var row = 0; row < 6; row++) {
		for (var column = 0; column < 4; column++) {
			if (gridData[row][column].player == currPlayer && gridData[row][column + 1].player == currPlayer && gridData[row][column + 2].player == currPlayer && gridData[row][column + 3].player == currPlayer) {
				return true;
			}
		}
	}
	// check vertical spaces
	for (var row = 0; row < 3; row++) {
		for (var column = 0; column < 7; column++) {
			if (gridData[row][column].player == currPlayer && gridData[row + 1][column].player == currPlayer && gridData[row + 2][column].player == currPlayer && gridData[row + 3][column].player == currPlayer) {
				return true;
			}
		}
	}
	// check / diagonal spaces
	for (var row = 0; row < 3; row++) {
		for (var column = 3; column < 7; column++) {
			if (gridData[row][column].player == currPlayer && gridData[row + 1][column - 1].player == currPlayer && gridData[row + 2][column - 2].player == currPlayer && gridData[row + 3][column - 3].player == currPlayer) {
				return true;
			}
		}
	}
	// check \ diagonal spaces
	for (var row = 0; row < 3; row++) {
		for (var column = 0; column < 4; column++) {
			if (gridData[row][column].player == currPlayer && gridData[row + 1][column + 1].player == currPlayer && gridData[row + 2][column + 2].player == currPlayer && gridData[row + 3][column + 3].player == currPlayer) {
				return true;
			}
		}
	}
	return false;
}

function checkTie() {
	var foundEmptySpace = true;
	for (var column = 0; column < 7; column++) {
		if (gridData[0][column].player == 0) {
			foundEmptySpace = false;
		}
	}
	return foundEmptySpace;
}

function dropCoin(column) {
	for (var row = 0; row < 6; row++) {
		if (gridData[row][column].player != 0) {
			gridData[row - 1][column].player = currPlayer;
			break;
		}
		if (row == 5 && gridData[row][column].player == 0) {
			gridData[row][column].player = currPlayer;
		}
	}

	if (checkWinner()) {
		if (currPlayer == player1) {
			document.getElementById("gameInfo").innerHTML = "";
			document.getElementById("gameInfo").innerHTML = "<h3>Spieler 1 gewinnt!</h3>";

		} else {
			document.getElementById("gameInfo").innerHTML = "";
			document.getElementById("gameInfo").innerHTML = "<h3>Spieler 2 gewinnt!</h3>";
		}
		gameEndedProcedure();
		return;
	}

	if (checkTie()) {
		document.getElementById("gameInfo").innerHTML = "";
		document.getElementById("gameInfo").innerHTML = "<h3>Unentschieden!</h3>";
		gameEndedProcedure();
	}

	if (currPlayer == player1) {
		currPlayer = player2;
	} else {
		currPlayer = player1;
	}
}

function gameEndedProcedure() {
	document.getElementById("grid").classList.add("disableAndOpacity");
	document.getElementById("startGame").classList.remove("disableAndOpacity");
	document.getElementById("startGame").innerText = "Neues Spiel";
	gameEnded = true;
}

/**
 * Handle AI vs AI situation
 */

function checkAiTurn() {
    if ((player1pickedSet && currPlayer == player1) || (player2pickedSet && currPlayer == player2)) {
        var response = getColumnFromServer();
        var resultCol = response.column;
        refreshColValues(response);
        if (typeof resultCol === 'undefined') {
            document.getElementById("gameInfo").innerHTML = "<h4>Fehler!</h4>";
            setTimeout(function () {
                document.getElementById("gameInfo").innerHTML = "";
            }, 1500);
        } else {
            var row = getNextRow(resultCol);
            var coords = getPos(document.getElementById("svgGrid"));
            var radius = gridData[row][resultCol].width;
            var x = gridData[row][resultCol].x + coords.x + radius / 2;
            var y = gridData[row][resultCol].y + coords.y + radius / 2;
            clickXY(x, y);
        }
    }
}

function getNextRow(column) {
    for (var row = 0; row < 6; row++) {
        if (gridData[row][column].player != 0) {
            return row - 1;
        }
        if (row == 5 && gridData[row][column].player == 0) {
            return row;
        }
    }
}

function clickXY(x, y) {
    var ev = new MouseEvent('click', {
        'view': window,
        'bubbles': true,
        'cancelable': true,
        'screenX': x,
        'screenY': y
    });
    var el = document.elementFromPoint(x, y);
    el.dispatchEvent(ev);
}

function getPos(element) {
    var rect = element.getBoundingClientRect();
    return {
        x: rect.left,
        y: rect.top
    };
}
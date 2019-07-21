/**
 * Communication with backend
 */

function createRequestData() {
	var jsonRequest = "";
	var jsonGrid = new Array();

	for (var row = 0; row < 6; row++) {
		jsonGrid.push(new Array());
		for (var col = 0; col < 7; col++) {
			jsonGrid[row].push(gridData[row][col].player);
		}
	}

	if (currPlayer == 1) {
		var gameMode1 = document.getElementById("gameMode1");
		var gameModeValue1 = gameMode1.options[gameMode1.selectedIndex].value;

		if (gameModeValue1 == "ql") {
			var depth = document.getElementById("deep1").value;
			var exp = document.getElementById("expSet1").value;
			var explo = document.getElementById("exploSet1").value;
			jsonRequest = JSON.stringify({
				"grid": jsonGrid,
				"player": currPlayer,
				"mode": "ql",
				"exp": exp,
				"explo": explo
			})
		}
		if (gameModeValue1 == "mm") {
			var depth = document.getElementById("deep1").value;
			jsonRequest = JSON.stringify({
				"grid": jsonGrid,
				"player": currPlayer,
				"mode": "mm",
				"depth": depth
			})
		}
		if (gameModeValue1 == "rb") {
			jsonRequest = JSON.stringify({
				"grid": jsonGrid,
				"player": currPlayer,
				"mode": "rb"
			})
		}
	} else {
		var gameMode2 = document.getElementById("gameMode2");
		var gameModeValue2 = gameMode2.options[gameMode2.selectedIndex].value;

		if (gameModeValue2 == "ql") {
			var depth = document.getElementById("deep2").value;
			var depth = document.getElementById("deep2").value;
			jsonRequest = JSON.stringify({
				"grid": jsonGrid,
				"player": currPlayer,
				"mode": "ql",
				"depth": depth
			})
		}
		if (gameModeValue2 == "mm") {
			var depth = document.getElementById("deep2").value;
			jsonRequest = JSON.stringify({
				"grid": jsonGrid,
				"player": currPlayer,
				"mode": "mm",
				"depth": depth
			})
		}
		if (gameModeValue2 == "rb") {
			jsonRequest = JSON.stringify({
				"grid": jsonGrid,
				"player": currPlayer,
				"mode": "rb"
			})
		}
	}
	return jsonRequest;
}

function getColumnFromServer() {
	var jsonResponse = "";

	var jsonRequest = createRequestData();
	console.log(jsonRequest);

	var request = new XMLHttpRequest();
	var xhr = new XMLHttpRequest();

	xhr.open("POST", '/data', false);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(jsonRequest);

	var response = xhr.response;

	try {
		jsonResponse = JSON.parse(response);
	} catch (err) {
		console.log(err);
	}

	console.log(jsonResponse);
	return jsonResponse.column;
}

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
	var foundEmptySpace = false;
	for (var row = 0; row < 6; row++) {
		for (var column = 0; column < 7; column++) {
			if (gridData[row][column].player == 0) {
				foundEmptySpace = true;
			}
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
		if (currPlayer == 1) {
			document.getElementById("gameInfo").innerHTML = "";
			document.getElementById("gameInfo").innerHTML = "<h3>Spieler 1 gewinnt!</h3>";

		} else {
			document.getElementById("gameInfo").innerHTML = "";
			document.getElementById("gameInfo").innerHTML = "<h3>Spieler 2 gewinnt!</h3>";
		}
		gameEndedProcedure();
	}

	if (!checkTie()) {
		document.getElementById("gameInfo").innerHTML = "";
		document.getElementById("gameInfo").innerHTML = "<h3>Unentschieden!</h3>";
		gameEndedProcedure();
	}

	if (currPlayer == 1) {
		currPlayer = 2;
	} else {
		currPlayer = 1;
	}
}

function gameEndedProcedure() {
	document.getElementById("grid").classList.add("disableAndOpacity");
	document.getElementById("startGame").classList.remove("disableAndOpacity");
	document.getElementById("startGame").innerText = "Neues Spiel";
	gameEnded = true;
}

/*
Main
*/
gridData = initGridData();
renderGrid();
$("#grid").addClass("disableAndOpacity");
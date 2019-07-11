var blueBoardColor = "#5087D1";
var redCoinColor = "#FB382E";
var yellowCoinColor = "#FBE92E";

// grid size definition
var box = document.getElementById("grid");
var width = box.offsetWidth;
var size = width / 9;
var gridWidth = size * 7 + 25;
var gridHeight = size * 6;
var gridData = null;

// move settings
var player1pickedSet = false;
var player2pickedSet = false;
var player1pickedHuman = false;
var player2pickedHuman = false;
var currPlayer = 1;
var continueGame = false;
var gameEnded = false;

class GameBoard {

}

class GameLogic {
	
}

/**
 * Funktionen
 */
function initGridData() {
	var data = new Array();
	var rowNum = 0;
	var colNum = 0;
	var xpos = 1;
	var ypos = 1;
	var width = size;
	var height = size;
	var player = 0;
	var mouseEvent = false;

	for (var row = 0; row < 6; row++) {
		data.push(new Array());
		for (var column = 0; column < 7; column++) {
			data[row].push({
				rowNum: row,
				colNum: column,
				x: xpos,
				y: ypos,
				width: width,
				height: height,
				player: player,
				mouseEvent: mouseEvent
			})
			// increment the x position. I.e. move it over by 50 (width variable)
			xpos += width;
		}
		// reset the x position after a row is complete
		xpos = 1;
		// increment the y position for the next row. Move it down 50 (height variable)
		ypos += height;
	}
	return data;
}

function renderGrid() {
	document.getElementById("grid").innerHTML = "";

	var grid = d3.select("#grid")
		.append("svg")
		.attr("id", "svgGrid")
		.attr("width", gridWidth)
		.attr("height", gridHeight);

	var row = grid.selectAll(".row")
		.data(gridData)
		.enter().append("g")
		.attr("class", "row");

	var column = row.selectAll(".square")
		.data(function (d) {
			return d;
		})
		.enter().append("rect")
		.attr("class", "rect")
		.attr("x", function (d) {
			return d.x;
		})
		.attr("y", function (d) {
			return d.y;
		})
		.attr("width", function (d) {
			return d.width;
		})
		.attr("height", function (d) {
			return d.height;
		})
		.style("fill", blueBoardColor)

	var circle = row.selectAll(".circle")
		.data(function (d) {
			return d;
		})
		.enter().append("circle")
		.attr("width", function (d) {
			return d.width;
		})
		.attr("height", function (d) {
			return d.height;
		})
		.attr("cx", function (d) {
			return d.x + d.width / 2;
		})
		.attr("cy", function (d) {
			return d.y + d.height / 2;
		})
		.attr("r", function (d) {
			return d.height / 2 * 0.8
		})
		.style("fill", function (d) {
			return getColor(d);
		})
		.on("mouseover", function (d) {
			if ((d.rowNum == 5) || (d.mouseEvent))
				handleMouseOver(d);
		})
		.on("mouseout", function (d) {
			if ((d.rowNum == 5) || (d.mouseEvent))
				handleMouseOut(d);
		})
		.on("click", function (d) {
			if ((d.rowNum == 5) || (d.mouseEvent)) {
				handleMouseClick();
				dropCoin(d.colNum);
				if (d.rowNum == 0)
					gridData[d.rowNum][d.colNum].mouseEvent = true;
				else
					gridData[d.rowNum - 1][d.colNum].mouseEvent = true;
				d3.select(d3.event.target).on("click", null);
				d3.select(d3.event.target).on("mouseover", null);
				d3.select(d3.event.target).on("mouseout", null);
				if (player1pickedSet && player2pickedSet) {
					setTimeout(function(){
						checkAiTurn();
					}, 1000);
				} else {
					checkAiTurn();
				}
			}
		});
}

function getColor(d) {
	if (d.player == 1) {
		return redCoinColor
	}
	if (d.player == 2) {
		return yellowCoinColor
	}
	return "#fff"
}

/**
 * Events für d3js
 *  */

function handleMouseClick() {
	if (currPlayer == 1) {
		d3.select(d3.event.target).style("fill", redCoinColor).style("opacity", 1);
	} else {
		d3.select(d3.event.target).style("fill", yellowCoinColor).style("opacity", 1);
	}
}

function handleMouseOver(d) {
	if (currPlayer == 1) {
		d3.select(d3.event.target).style("fill", redCoinColor).style("opacity", 1);
	} else {
		d3.select(d3.event.target).style("fill", yellowCoinColor).style("opacity", 1);
	}
}

function handleMouseOut(d) {
	d3.select(d3.event.target).style("fill", "#fff").style("opacity", 1);
}

function MouseOver(elem) {
	elem.style.color = "red";
}

function MouseOut(elem) {
	elem.style.color = "yellow";
}

function resizeGrid() {
	var newGrid = document.getElementById("grid");
	var newWidth = newGrid.offsetWidth / 9;

	gridWidth = newWidth * 7 + 25;
	gridHeight = newWidth * 6;

	xpos = 1;
	ypos = 1;

	for (var row = 0; row < 6; row++) {
		for (var column = 0; column < 7; column++) {
			gridData[row][column].x = xpos;
			gridData[row][column].y = ypos;
			gridData[row][column].width = newWidth;
			gridData[row][column].height = newWidth;
			xpos += newWidth;
		}
		xpos = 1;
		ypos += newWidth;
	}
	renderGrid();
}

/**
 * Event listener für alle nicht d3js Elemente
 */

document.getElementById("player1robot").addEventListener("click", function () {
	document.getElementById("playerPickBox1").style.display = "none";
	document.getElementById("settingsAiTemplate1").style.display = "block";
	document.getElementById("confirmTemplate1").style.display = "block";
});

document.getElementById("player1human").addEventListener("click", function () {
	document.getElementById("playerPickBox1").style.display = "none";
	document.getElementById("humanTemplate1").style.display = "block";
	document.getElementById("back3").style.display = "block";
	player1pickedHuman = true;
});

document.getElementById("player2robot").addEventListener("click", function () {
	document.getElementById("playerPickBox2").style.display = "none";
	document.getElementById("settingsAiTemplate2").style.display = "block";
	document.getElementById("confirmTemplate2").style.display = "block";
});

document.getElementById("player2human").addEventListener("click", function () {
	document.getElementById("playerPickBox2").style.display = "none";
	document.getElementById("humanTemplate2").style.display = "block";
	document.getElementById("back4").style.display = "block";
	player2pickedHuman = true;
});

document.getElementById("confirmBtn1").addEventListener("click", function () {
	document.getElementById("settingsAiTemplate1").style.display = "none";
	document.getElementById("confirmTemplate1").style.display = "none";
	document.getElementById("aiTemplate1").style.display = "block";
	document.getElementById("back3").style.display = "block";

	var tempGameMode = document.getElementById("gameMode1");
	document.getElementById("setList1").innerHTML = "";
	if (tempGameMode.value == "ql") {
		var tempExpSet = document.getElementById("expSet1").value;
		var tempExploSet = document.getElementById("exploSet1").value;
		document.getElementById("setList1").innerHTML += "<p>Q-Learning</p>"
		document.getElementById("setList1").innerHTML += "<p>" + tempExpSet + "</p>"
		document.getElementById("setList1").innerHTML += "<p>" + tempExploSet + "</p>"
	}
	if (tempGameMode.value == "mm") {
		var tempTreeDepth = document.getElementById("deep1").value;
		document.getElementById("setList1").innerHTML += "<p>Minimax</p>"
		document.getElementById("setList1").innerHTML += "<p>" + tempTreeDepth + "</p>"
	}

	player1pickedSet = true;
});

document.getElementById("confirmBtn2").addEventListener("click", function () {
	document.getElementById("settingsAiTemplate2").style.display = "none";
	document.getElementById("confirmTemplate2").style.display = "none";
	document.getElementById("aiTemplate2").style.display = "block";
	document.getElementById("back4").style.display = "block";

	var tempGameMode = document.getElementById("gameMode2");
	document.getElementById("setList2").innerHTML = "";
	if (tempGameMode.value == "ql") {
		var tempExpSet = document.getElementById("expSet2").value;
		var tempExploSet = document.getElementById("exploSet2").value;
		document.getElementById("setList2").innerHTML += "<p>Q Learning</p>"
		document.getElementById("setList2").innerHTML += "<p>" + tempExpSet + "</p>"
		document.getElementById("setList2").innerHTML += "<p>" + tempExploSet + "</p>"
	}
	if (tempGameMode.value == "mm") {
		var tempTreeDepth = document.getElementById("deep2").value;
		document.getElementById("setList2").innerHTML += "<p>Minimax</p>"
		document.getElementById("setList2").innerHTML += "<p>" + tempTreeDepth + "</p>"
	}
	player2pickedSet = true;
});

document.getElementById("back1").addEventListener("click", function () {
	document.getElementById("settingsAiTemplate1").style.display = "none";
	document.getElementById("confirmTemplate1").style.display = "none";
	document.getElementById("playerPickBox1").style.display = "block";
});

document.getElementById("back2").addEventListener("click", function () {
	document.getElementById("settingsAiTemplate2").style.display = "none";
	document.getElementById("confirmTemplate2").style.display = "none";
	document.getElementById("playerPickBox2").style.display = "block";
});

document.getElementById("back3").addEventListener("click", function () {
	if (player1pickedHuman) {
		document.getElementById("humanTemplate1").style.display = "none";
		document.getElementById("back3").style.display = "none";
		document.getElementById("playerPickBox1").style.display = "block";
		player1pickedHuman = false;
		document.getElementById("grid").classList.add("disableAndOpacity");
		document.getElementById("startGame").classList.remove("disableAndOpacity");
		if (!gameEnded)
			document.getElementById("startGame").innerText = "Spiel fortsetzen";
	} else {
		document.getElementById("back3").style.display = "none";
		document.getElementById("aiTemplate1").style.display = "none";
		document.getElementById("confirmTemplate1").style.display = "block";
		document.getElementById("settingsAiTemplate1").style.display = "block";
		player1pickedSet = false;
		document.getElementById("grid").classList.add("disableAndOpacity");
		document.getElementById("startGame").classList.remove("disableAndOpacity");
		if (!gameEnded)
			document.getElementById("startGame").innerText = "Spiel fortsetzen";
	}
});

document.getElementById("back4").addEventListener("click", function () {
	if (player2pickedHuman) {
		document.getElementById("humanTemplate2").style.display = "none";
		document.getElementById("back4").style.display = "none";
		document.getElementById("playerPickBox2").style.display = "block";
		player2pickedHuman = false;
		document.getElementById("grid").classList.add("disableAndOpacity");
		if (!gameEnded)
			document.getElementById("startGame").innerText = "Spiel fortsetzen";
	} else {
		document.getElementById("back4").style.display = "none";
		document.getElementById("aiTemplate2").style.display = "none";
		document.getElementById("confirmTemplate2").style.display = "block";
		document.getElementById("settingsAiTemplate2").style.display = "block";
		player2pickedSet = false;
		document.getElementById("grid").classList.add("disableAndOpacity");
		if (!gameEnded)
			document.getElementById("startGame").innerText = "Spiel fortsetzen";
	}
});

document.getElementById("gameMode1").addEventListener("change", function () {
	if (this.value == "rb") {
		document.getElementById("expSet1Box").style.display = "none";
		document.getElementById("exploSet1Box").style.display = "none";
		document.getElementById("deep1Box").style.display = "none";
	}
	if (this.value == "mm") {
		document.getElementById("expSet1Box").style.display = "none";
		document.getElementById("exploSet1Box").style.display = "none";
		document.getElementById("deep1Box").style.display = "block";
	}
	if (this.value == "ql") {
		document.getElementById("deep1Box").style.display = "none";
		document.getElementById("expSet1Box").style.display = "block";
		document.getElementById("exploSet1Box").style.display = "block";
	}
});

document.getElementById("gameMode2").addEventListener("change", function () {
	if (this.value == "rb") {
		document.getElementById("expSet2Box").style.display = "none";
		document.getElementById("exploSet2Box").style.display = "none";
		document.getElementById("deep2Box").style.display = "none";
	}
	if (this.value == "mm") {
		document.getElementById("expSet2Box").style.display = "none";
		document.getElementById("exploSet2Box").style.display = "none";
		document.getElementById("deep2Box").style.display = "block";
	}
	if (this.value == "ql") {
		document.getElementById("deep2Box").style.display = "none";
		document.getElementById("expSet2Box").style.display = "block";
		document.getElementById("exploSet2Box").style.display = "block";
	}
});

document.getElementById("delete").addEventListener("click", function () {
	location.reload();
});

document.getElementById("startGame").addEventListener("click", function () {

	if ((player1pickedSet || player1pickedHuman) && (player2pickedSet || player2pickedHuman)) {
		document.getElementById("startGame").classList.add("disableAndOpacity");

		if (gameEnded) {
			document.getElementById("gameInfo").innerHTML = "";
			gridData = initGridData();
			renderGrid();
			gameEnded = false;
		}

		if (continueGame) {
			document.getElementById("startGame").innerText = "Spiel starten";
			document.getElementById("grid").classList.remove("disableAndOpacity");
			continueGame = false;
			if ((player1pickedSet && player2pickedHuman) || (player1pickedSet && player2pickedSet)) {
				checkAiTurn();
			}
		} else {
			document.getElementById("grid").classList.remove("disableAndOpacity");
			continueGame = true;

			if ((player1pickedSet && player2pickedHuman) || (player1pickedSet && player2pickedSet)) {
				checkAiTurn();
			}
		}
	} else {
		//alert("Ein neues Spiel kann erst gestartet werden, wenn beide Spieler ihre Einstellungen bestätigt haben.");
		$("#settingsModal").modal()
	}
});

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

function gameEndedProcedure() {
	document.getElementById("grid").classList.add("disableAndOpacity");
	document.getElementById("startGame").classList.remove("disableAndOpacity");
	document.getElementById("startGame").innerText = "Neues Spiel";
	gameEnded = true;
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

function checkAiTurn() {
	if ((player1pickedSet && currPlayer == 1) || (player2pickedSet && currPlayer == 2)) {
		var resultCol = getColumnFromServer();
		if (typeof resultCol === 'undefined') {
			document.getElementById("gameInfo").innerHTML = "<h4>Es ist ein Fehler aufgetreten</h4>";
			setTimeout(function(){
				document.getElementById("gameInfo").innerHTML = "";
			}, 5000);
		} else {
			var row = getNextRowByCol(resultCol);
			var coords = getPos(document.getElementById("svgGrid"));
			var radius = gridData[row][resultCol].width;
			var x = gridData[row][resultCol].x + coords.x + radius/2;
			var y = gridData[row][resultCol].y + coords.y +radius/2;
			clickXY(x,y);
		}
	}
}

function getNextRowByCol(column) {
	for (var row = 0; row < 6; row++) {
		if (gridData[row][column].player != 0) {
			return row-1;
			break;
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
	return {x:rect.left,y:rect.top};
}

/**
 * Main
 */

window.addEventListener('resize', resizeGrid);

//TODO
/*window.addEventListener("beforeunload", function(event) {
    event.returnValue = "Your custom message.";
});*/

$('[data-toggle="tooltip"]').tooltip({
	delay: {
		show: 500,
		hide: 0
	}
})

$('.toolEvent').on('click', function () {
	$(this).tooltip('hide')
})

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
	console.log("JSON: "+ jsonRequest);

	var request = new XMLHttpRequest(); 
	var xhr = new XMLHttpRequest();

	xhr.open("POST", '/data', false);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(jsonRequest);

	var response = xhr.response;

	try {
		jsonResponse = JSON.parse(response);
	  }
	  catch(err) {
		  console.log(err);
	  }

	console.log(jsonResponse);
	return jsonResponse.column;
}

/*
Main
*/
gridData = initGridData();
renderGrid();
$("#grid").addClass("disableAndOpacity");
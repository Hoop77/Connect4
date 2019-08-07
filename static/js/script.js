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

		if (gameModeValue1 == "td") {
			var depth = document.getElementById("deep1").value;
			var exp = document.getElementById("expSet1").value;
			jsonRequest = JSON.stringify({
				"grid": jsonGrid,
				"player": currPlayer,
				"mode": "td",
				"exp": exp,
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

		if (gameModeValue2 == "td") {
			var depth = document.getElementById("deep2").value;
			var depth = document.getElementById("deep2").value;
			jsonRequest = JSON.stringify({
				"grid": jsonGrid,
				"player": currPlayer,
				"mode": "td",
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
	return jsonResponse;
}

/*
Main
*/
gridData = initGridData();
renderGrid();
colValuesData = initColValuesData();
renderColValues();
$("#grid").addClass("disableAndOpacity");
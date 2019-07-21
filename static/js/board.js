var blueBoardColor = "#5087D1";
var redCoinColor = "#FB382E";
var yellowCoinColor = "#FBE92E";

// grid size definition
var box = document.getElementById("grid");
var size = box.offsetWidth / 9;
var gridWidth = size * 7 + 25;
var gridHeight = size * 6;
var gridData = null;

/**
 * D3.js data init and rendering
 */
function initGridData() {
    var data = new Array();
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
                    setTimeout(function () {
                        checkAiTurn();
                    }, 5000);
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
 * Handle AI vs AI situation
 */

function checkAiTurn() {
	if ((player1pickedSet && currPlayer == 1) || (player2pickedSet && currPlayer == 2)) {
        var resultCol = getColumnFromServer();
		if (typeof resultCol === 'undefined') {
			document.getElementById("gameInfo").innerHTML = "<h4>Fehler!</h4>";
			setTimeout(function () {
				document.getElementById("gameInfo").innerHTML = "";
			}, 5000);
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
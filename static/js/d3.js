var blueBoardColor = "#5087D1";
var redCoinColor = "#FB382E";
var yellowCoinColor = "#FBE92E";

var player1 = 1;
var player2 = -1;

// grid size definition
var box = document.getElementById("grid");
var size = box.offsetWidth / 9;
var gridWidth = size * 7 + 25;
var gridHeight = size * 6;
var gridData = null;
var colValuesData = null;

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
                if (gameEnded == false) {
                    if (player1pickedSet && player2pickedSet) {
                        setTimeout(function () {
                            checkAiTurn();
                        }, 1500);
                    } else {
                        checkAiTurn();
                    }
                }
            }
        });
}

function getColor(d) {
    if (d.player == 1) {
        return redCoinColor
    }
    if (d.player == -1) {
        return yellowCoinColor
    }
    return "#fff"
}

function handleMouseClick() {
    if (currPlayer == player1) {
        d3.select(d3.event.target).style("fill", redCoinColor).style("opacity", 1);
    } else {
        d3.select(d3.event.target).style("fill", yellowCoinColor).style("opacity", 1);
    }
}

function handleMouseOver(d) {
    if (currPlayer == player1) {
        d3.select(d3.event.target).style("fill", redCoinColor).style("opacity", 1);
    } else {
        d3.select(d3.event.target).style("fill", yellowCoinColor).style("opacity", 1);
    }
}

function handleMouseOut(d) {
    d3.select(d3.event.target).style("fill", "#fff").style("opacity", 1);
}

/**
 * D3.js data init and rendering for column values
 */
function initColValuesData() {
    var data = new Array();
    var xpos = 1;
    var ypos = 1;
    var width = size;
    var height = size;
    var text = "";

    for (var row = 0; row < 1; row++) {
        data.push(new Array());
        for (var column = 0; column < 7; column++) {
            data[row].push({
                x: xpos,
                y: ypos,
                width: width,
                height: height,
                text: text
            })
            xpos += width;
        }
        xpos = 1;
        ypos += height;
    }
    return data;
}

function renderColValues() {
    coLValuesHeight = size
    document.getElementById("colValues").innerHTML = "";

    var colValues = d3.select("#colValues")
        .append("svg")
        .attr("width", gridWidth)
        .attr("height", coLValuesHeight);

    var row = colValues.selectAll(".row")
        .data(colValuesData)
        .enter().append("g")
        .attr("class", "row")
        .style("fill", "#fff");

    var text = row.selectAll(".text")
        .data(function (d) {
            return d;
        })
        .enter().append("text")
        .attr("width", function (d) {
            return d.width;
        })
        .attr("height", function (d) {
            return d.height;
        })
        .attr("x", function (d) {
            return d.x + d.width / 2;
        })
        .attr("y", function (d) {
            return d.y + d.height / 1.5;
        })
        .text(function (d) {
            return d.text;
        })
        .style("fill", "black")
        .style("font-size", "2em")
}

function resizeGridAndColValues() {
    var newGrid = document.getElementById("grid");
    var newWidth = newGrid.offsetWidth / 9;

    size = newWidth;
    gridWidth = newWidth * 7 + 25;
    gridHeight = newWidth * 6;

    xpos = 1;
    ypos = 1;

    for (var row = 0; row < 6; row++) {
        for (var column = 0; column < 7; column++) {
            if (row == 0) {
                colValuesData[row][column].x = xpos;
                colValuesData[row][column].y = ypos;
                colValuesData[row][column].width = newWidth;
                colValuesData[row][column].height = newWidth;
            }
            gridData[row][column].x = xpos;
            gridData[row][column].y = ypos;
            gridData[row][column].width = newWidth;
            gridData[row][column].height = newWidth;
            xpos += newWidth;
        }
        xpos = 1;
        ypos += newWidth;
    }
    renderColValues();
    renderGrid();
}

function refreshColValues(response) {
    if (Object.keys(response).length == 1) {
        for (var row = 0; row < 1; row++) {
            for (var column = 0; column < 7; column++) {
                colValuesData[row][column].text = "";
            }
        }
    } else {
        colValuesData[0][0].text = response.col0;
        colValuesData[0][1].text = response.col1;
        colValuesData[0][2].text = response.col2;
        colValuesData[0][3].text = response.col3;
        colValuesData[0][4].text = response.col4;
        colValuesData[0][5].text = response.col5;
        colValuesData[0][6].text = response.col6;
    }
    renderColValues();
}
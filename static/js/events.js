// setting flags
var player1pickedSet = false;
var player2pickedSet = false;
var player1pickedHuman = false;
var player2pickedHuman = false;
var currPlayer = 1;
var continueGame = false;
var gameEnded = false;

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
            currPlayer = 1;
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
        $("#settingsModal").modal()
    }
});

window.addEventListener('resize', resizeGrid);

$('[data-toggle="tooltip"]').tooltip({
    delay: {
        show: 500,
        hide: 0
    }
})

$('.toolEvent').on('click', function () {
    $(this).tooltip('hide')
})

//TODO
/*window.addEventListener("beforeunload", function(event) {
    event.returnValue = "Your custom message.";
});*/
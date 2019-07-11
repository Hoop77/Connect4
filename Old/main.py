import sys
import simplejson as json
from flask import Flask, render_template, request
import numpy as np
from model import *

app = Flask(__name__)

# global
isGameOver = False
isPlayerOne = True

ENV = None
AGENT = None

def initGame():
	global AGENT, ENV
	ENV = Environment()
	AGENT = Agent(ENV)

def consoleMode():
	global isPlayerOne
	global isGameOver

	while(True):
		env = Environment()
		player1 = Agent(env)
		player2 = Agent(env)
		
		print("New Game")
		
		isGameOver = False
		while not isGameOver:
			board = env.getState()
			printBoard(board)
			if isPlayerOne:
				print("Player 1")
				col = int(input("Choose a column 0-6: "))
				player1.humanAction(col)
				isPlayerOne = False
			else:
				print("Player 2")
				player2.action()
				isPlayerOne = True
				
			print("GameOver:", isGameOver)

def serverMode():
	app.run(debug=True, use_reloader=False) #host='0.0.0.0',port=5000, 

@app.route("/")
def index():
	return render_template('index.html')
	
@app.route('/data', methods=['POST'])
def data():
	gridData = request.json['grid']
	currPlayer = request.json['player']
	currBoard = np.array(gridData)
	ENV.setState(currBoard)
	
	resultCol = AGENT.action(currPlayer)
	#print("Resultcol", resultCol)
	
	responseData = {"column": resultCol}
	jsonResponse = json.dumps(responseData)
	#print("JsonResponse: ", jsonResponse)
	
	return jsonResponse

def printBoard(board):
	fliped = np.flip(board,0)
	for x in range(0, 6):
		print("\n")
		for y in range(0, 7):
			if fliped[x,y] == 0:
				print("  .", end="  ")
			elif fliped[x,y] == 1:
				print("  X", end="  ")
			elif fliped[x,y] == 2:
				print("  O", end="  ")
		if x == 5:
			print("\n\n  0    1    2    3    4    5    6\n\n")

def main():
	initGame()
	
	print("\n1. Server mode")
	print("2. Training mode")
	print("3. Console mode\n")
	mode = int(input("Choose your mode: "))

	if mode == 1:
		print("\nYou picked the server mode!\n")
		serverMode()
	elif mode == 2:
		print("\nYou picked the training mode!\n")
	elif mode == 3:
		print("\nYou picked the console mode!\n")
		consoleMode()

if __name__ == '__main__':
	main()
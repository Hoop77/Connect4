import sys
import simplejson as json
from flask import Flask, render_template, request
import numpy as np
from agent import DQNAgent
from environment import STATE_SHAPE, NUM_ACTIONS

app = Flask(__name__)

def serverMode():
	app.run(debug=True, use_reloader=False) #host='0.0.0.0',port=5000, 

def choose_column(request, board):
	col = -1	
	currPlayer = request.json['player']
	
	if request.json['mode'] == "ql":
		#exp = int(request.json['exp'])
		#explo = float(request.json['explo'])
		agent = DQNAgent()
		agent.load('') # TODO
		col = agent.act(board)
	if request.json['mode'] == "mm":
		depth = int(request.json['depth'])
		col, minimax_score = minimax(board, depth, -math.inf, math.inf, True, currPlayer)
	if request.json['mode'] == "rb":
		col = randomBlock(board, currPlayer)
		
	return col

@app.route("/")
def index():
	return render_template('index.html')
	
@app.route('/data', methods=['POST'])
def data():
	gridData = request.json['grid']
	board = np.array(gridData)
	choice = choose_column(request, board)
	responseData = {"column": choice}
	jsonResponse = json.dumps(responseData)
	
	return jsonResponse

def main():	
	print("\n1. Server mode")
	print("2. Training mode")
	mode = int(input("Choose your mode: "))

	if mode == 1:
		print("\nYou picked the server mode!\n")
		serverMode()
	elif mode == 2:
		print("\nYou picked the training mode!\n")

if __name__ == '__main__':
	main()
import sys
import simplejson as json
from flask import Flask, render_template, request
import numpy as np
np.random.seed(0)
from agent import DQNAgent
from train import train
from policy import minimax, random_block, random_choice
import math
import tensorflow as tf
import board

app = Flask(__name__)

params = {
	'agent_params': {
		'memory_size': 2000,
		'gamma': 0.9,
		'epsilon': 1.0,
		'epsilon_min': 0.1,
		'epsilon_decay': 0.999,
		'batch_size': 32,
		'update_interval': 100,
		'num_epochs': 5,
		'learning_rate': 0.001
	},
	'num_episodes': 30000,
	#'opponent_policy': lambda state: minimax(state, 3, -math.inf, math.inf, True, board.YELLOW)[0]
	'opponent_policy': random_choice
}

session = tf.Session()
graph = tf.get_default_graph()
with graph.as_default():
	with session.as_default():
		agent = DQNAgent(**params)

def serverMode():
	app.run(debug=True, use_reloader=False) #host='0.0.0.0',port=5000, 

def choose_column(request, board):
	col = -1	
	currPlayer = request.json['player']
	
	if request.json['mode'] == "ql":
		#exp = int(request.json['exp'])
		#explo = float(request.json['explo'])
		with graph.as_default():
			with session.as_default():
				print(np.round(agent.predict(board), 3))
				agent.load('models/model.h5')
				col = agent.act(board)
	if request.json['mode'] == "mm":
		depth = int(request.json['depth'])
		col, minimax_score = minimax(board, depth, -math.inf, math.inf, True, currPlayer)
	if request.json['mode'] == "rb":
		col, _ = random_block(board, currPlayer)
		
	return col

@app.route("/")
def index():
	return render_template('index.html')
	
@app.route('/data', methods=['POST'])
def data():
	gridData = request.json['grid']
	board = np.array(gridData)
	col = choose_column(request, board)
	responseData = {"column": int(col)}
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
		train(model_path='models/model.h5', **params)

if __name__ == '__main__':
	main()
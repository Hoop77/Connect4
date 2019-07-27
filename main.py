import sys
import simplejson as json
from flask import Flask, render_template, request
import numpy as np
np.random.seed(0)
from agent import Agent
from train import train
from policy import minimax, random_block, random_choice
import math
import tensorflow as tf
import board

app = Flask(__name__)

args = {
	'agent_args': {
		'num_epochs': 1,
		'learning_rate': 0.01
	},
	'self_play_args': {
		'gamma': 0.95,
		'epsilon': 0.2
	},
	'resume_training': True,
	'num_episodes': 1000000,
	'life_plot': False
}

session = tf.Session()
graph = tf.get_default_graph()
with graph.as_default():
	with session.as_default():
		agent = Agent(**args)

def serverMode():
	app.run(debug=True, use_reloader=False) #host='0.0.0.0',port=5000, 

def choose_column(request, board):
	col = -1	
	player = request.json['player']

	if request.json['mode'] == "ql":
		#exp = int(request.json['exp'])
		#explo = float(request.json['explo'])
		with graph.as_default():
			with session.as_default():
				agent.load('models/model.h5')
				col, _, _ = agent.act(board, player)
	if request.json['mode'] == "mm":
		depth = int(request.json['depth'])
		col, minimax_score = minimax(board, depth, -math.inf, math.inf, True, player)
	if request.json['mode'] == "rb":
		col = random_block(board, player)
		
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
		train(model_path='models/model.h5', **args)

if __name__ == '__main__':
	main()
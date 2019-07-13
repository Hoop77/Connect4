import sys
import simplejson as json
from flask import Flask, render_template, request
import numpy as np
np.random.seed(0)
from agent import DQNAgent
from environment import STATE_SHAPE, NUM_ACTIONS
from train import train
from policy import minimax, random_block
import math
import tensorflow as tf

app = Flask(__name__)

session = tf.Session()
graph = tf.get_default_graph()
with graph.as_default():
	with session.as_default():
		agent = DQNAgent()
		agent.load('models/model.h5')

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
		train(model_path='models/model.h5', batch_size=32, num_episodes=1000)

if __name__ == '__main__':
	main()
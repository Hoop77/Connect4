import sys
import json
import numpy as np
from flask import Flask, render_template, request
np.random.seed(0)
from agent import Agent
from train import train
from policy import minimax, random_block, random_choice
import math
import tensorflow as tf
import board
from statistics import Stats
import tkinter as tk
from tkinter import filedialog

app = Flask(__name__)

args = {} # loaded from config.json

session = tf.Session()
graph = tf.get_default_graph()
with graph.as_default():
	with session.as_default():
		agent = Agent(**args)

def serverMode():
	app.run(debug=True, use_reloader=False) #host='0.0.0.0',port=5000, 

def calculate_response(request, board):
	col = -1
	free_cols = []
	col_values = []
	response_data = {}
	player = request.json['player']

	if request.json['mode'] == "td":
		#exp = int(request.json['exp'])
		#explo = float(request.json['explo'])
		with graph.as_default():
			with session.as_default():
				agent.load(args['file_name'])
				col, free_cols, col_values = agent.act(board, player)
				return generate_response_json(col, free_cols, col_values, player)
	if request.json['mode'] == "mm":
		depth = int(request.json['depth'])
		col, _ = minimax(board, depth, -math.inf, math.inf, True, player)
		return {"column": int(col)}
	if request.json['mode'] == "rb":
		col = random_block(board, player)
		return {"column": int(col)}
		
	return generate_response_json(col, free_cols, col_values)

def generate_response_json(col, free_cols, col_values, player):
	response_data = {"column": int(col)}
	temp = []
	if(player == board.PLAYER_1):
		temp = (-col_values).argsort()
	else:
		temp = col_values.argsort()
	ranks = np.empty_like(temp)
	ranks[temp] = np.arange(len(col_values))
	for i in range(0, len(free_cols)):
		response_data["col"+str(free_cols[i])] = int(ranks[i] + 1) # start from 0 to 1

	return response_data

@app.route("/")
def index():
	return render_template('index.html')
	
@app.route('/data', methods=['POST'])
def data():
	gridData = request.json['grid']
	board = np.array(gridData)
	response_data = calculate_response(request, board)
	jsonResponse = json.dumps(response_data)
	
	return jsonResponse

def get_config_json():
	with open('config.json') as json_file:
		data = json.load(json_file)
		return data['args']

def main():
	global args
	args = get_config_json()
	print("\n1. Server mode")
	print("2. Training mode")
	print("3. Plot stats")
	mode = int(input("Choose your mode: "))

	if mode == 1:
		print("\nYou picked the server mode!\n")
		serverMode()
	elif mode == 2:
		print("\nYou picked the training mode!\n")
		if args['create_stats']:
			stats = Stats(args)
			train(stats, **args)
		else:
			train(**args)
	elif mode == 3:
		print("\nYou picked the statistics mode!\n")
		root = tk.Tk()
		root.withdraw()
		file_path = filedialog.askopenfilename()
		stats = Stats()
		stats.plot_stats(file_path)

if __name__ == '__main__':
	main()
import sys
import json
import numpy as np
from flask import Flask, render_template, request
np.random.seed(0)
from agent import Agent
from train import train
from policy import minimax, random_block, random_choice
import math
import board
import tensorflow as tf
from statistics import Stats
import tkinter as tk
from tkinter import filedialog

app = Flask(__name__)

args = {} # loaded from config.json

# tensorflow need to have everything on same thread
session = tf.Session()
graph = tf.get_default_graph()
with graph.as_default():
	with session.as_default():
		agent = Agent(**args)

# start frontend as web application
def serverMode(ip, port):
	app.run(debug=True, use_reloader=False, host=ip, port=port)

def calculate_response(request, state):
	col = -1
	free_cols = []
	col_values = []
	response_data = {}
	player = request.json['player']

	if request.json['mode'] == "sp":
		exp = request.json['exp']
		file_name = "models/selfplay" + exp + ".h5"
		with graph.as_default():
			with session.as_default():
				agent.load(file_name)
				col, free_cols, col_values = agent.act(state, player)
				return generate_response_json(col, free_cols, col_values, player)
	if request.json['mode'] == "mm":
		depth = int(request.json['depth'])
		col, _ = minimax(state, depth, -math.inf, math.inf, True, player)
		return {"column": int(col)}
	if request.json['mode'] == "rb":
		col = random_block(state, player)
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

# frontend hosting
@app.route("/")
def index():
	return render_template('index.html')
	
# endpoint for communication between front- and backend
@app.route('/data', methods=['POST'])
def data():
	gridData = request.json['grid']
	state = np.array(gridData)
	response_data = calculate_response(request, state)
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
		ip = input("IP-Address (localhost=127.0.0.1): \n")
		port = int(input("Port (default=5000): \n"))
		serverMode(ip, port)
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
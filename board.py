import math
import numpy as np

NUM_ROWS = 6
NUM_COLS = 7

STATE_SHAPE = (NUM_ROWS, NUM_COLS)
NUM_ACTIONS = NUM_COLS

FREE = 0
RED = 1
YELLOW = 2

REWARD_WIN = 1
REWARD_DEFEAT = -1
REWARD_DRAW = 0.25 # TODO try out

def drop_piece(board, col, player):
	for row in range(0, NUM_ROWS):
		if board[row][col] != 0:
			board[row-1][col] = player
			break
		if row == 5 and board[row][col] == 0:
			board[row][col] = player
	
def get_free_columns(board):
	free_cols = []
	for col in range(0, NUM_COLS):
		if board[0][col] == 0:
			free_cols.append(col)
	return free_cols
	
def check_for_winner(board, player):
	# check horizontal spaces
	for x in range(0, 6):
		for y in range(0, 4):
			if board[x][y] == player and board[x][y+1] == player and board[x][y+2] == player and board[x][y+3] == player:
				return True

	# check vertical spaces
	for x in range(0, 3):
		for y in range(0, 7):
			if board[x][y] == player and board[x+1][y] == player and board[x+2][y] == player and board[x+3][y] == player:
				return True

	# check / diagonal spaces
	for x in range(0, 3):
		for y in range(3, 7):
			if board[x][y] == player and board[x+1][y-1] == player and board[x+2][y-2] == player and board[x+3][y-3] == player:
				return True

	# check \ diagonal spaces
	for x in range(0, 3):
		for y in range(0, 4):
			if board[x][y] == player and board[x+1][y+1] == player and board[x+2][y+2] == player and board[x+3][y+3] == player:
				return True
	return False
	
def check_terminal_node(board):
	return check_for_winner(board, 1) or check_for_winner(board, 2) or len(get_free_columns(board)) == 0
	
def evaluate_section(toEvaluate, currPlayer):
	score = 0
	free = 0
	enemy = -1
	
	if currPlayer == 1:
		enemy = 2
	else:
		enemy = 1

	if toEvaluate.count(currPlayer) == 4:
		score += 100
	elif toEvaluate.count(currPlayer) == 3 and toEvaluate.count(free) == 1:
		score += 5
	elif toEvaluate.count(currPlayer) == 2 and toEvaluate.count(free) == 2:
		score += 2

	if toEvaluate.count(enemy) == 3 and toEvaluate.count(free) == 1:
		score -= 4

	toEvaluate.clear()
	return score

def score_position(board, currPlayer):
	score = 0
	toEvaluate = []

	# Score center to preference the middle at the beginning
	center = [int(i) for i in list(board[:, 3])]
	centerCount = center.count(currPlayer)
	score += centerCount * 3

	# score horizontal spaces			
	for x in range(0, 6):
		for y in range(0, 4):
			toEvaluate.append(board[x][y])
			toEvaluate.append(board[x][y+1])
			toEvaluate.append(board[x][y+2])
			toEvaluate.append(board[x][y+3])
			score += evaluate_section(toEvaluate, currPlayer)

	# score vertical spaces
	for x in range(0, 3):
		for y in range(0, 7):
			toEvaluate.append(board[x][y])
			toEvaluate.append(board[x+1][y])
			toEvaluate.append(board[x+2][y])
			toEvaluate.append(board[x+3][y])
			score += evaluate_section(toEvaluate, currPlayer)

	# score / diagonal spaces
	for x in range(0, 3):
		for y in range(3, 7):
			toEvaluate.append(board[x][y])
			toEvaluate.append(board[x+1][y-1])
			toEvaluate.append(board[x+2][y-2])
			toEvaluate.append(board[x+3][y-3])
			score += evaluate_section(toEvaluate, currPlayer)

	# score \ diagonal spaces
	for x in range(0, 3):
		for y in range(0, 4):
			toEvaluate.append(board[x][y])
			toEvaluate.append(board[x+1][y+1])
			toEvaluate.append(board[x+2][y+2])
			toEvaluate.append(board[x+3][y+3])
			score += evaluate_section(toEvaluate, currPlayer)

	return score

def choose_best_action(board, values):
	avail_actions = get_free_columns(board) # assume sorted
	avail_idx = 0
	best_actions = []
	Q_max = -math.inf
	for action in range(NUM_ACTIONS):
		if avail_idx >= len(avail_actions):
			break
		if action == avail_actions[avail_idx]:
			Q = round(values[action], 5)
			if Q > Q_max:
				Q_max = Q
				best_actions = [(action)]
			elif Q == Q_max:
				best_actions.append(action)
			avail_idx += 1
	return np.random.choice(best_actions)
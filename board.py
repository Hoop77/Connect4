import math
import numpy as np

NUM_ROWS = 6
NUM_COLS = 7

STATE_SHAPE = (NUM_ROWS, NUM_COLS)
NUM_ACTIONS = NUM_COLS

FREE = 0
PLAYER_1 = 1
PLAYER_2 = -1

OUTCOME_NONE = 0
OUTCOME_WIN = 1
OUTCOME_DEFEAT = 2
OUTCOME_DRAW = 3

def drop_piece(board, col, player):
	board = board.copy()
	drop_piece_inplace(board, col, player)
	return board

def drop_piece_inplace(board, col, player):
	assert(board[0][col] == FREE)
	for row in reversed(range(NUM_ROWS)):
		if board[row][col] == FREE:
			board[row][col] = player
			break

def get_free_columns(board):
	return [col for col in range(NUM_COLS) if board[0][col] == 0]
	
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
	enemy = PLAYER_2
	
	if currPlayer == PLAYER_1:
		enemy = PLAYER_2
	else:
		enemy = PLAYER_1

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

def get_outcome_after_move(board, player):
	if check_for_winner(board, player):
		return OUTCOME_WIN if player == PLAYER_1 else OUTCOME_DEFEAT
	elif len(get_free_columns(board)) == 0:
		return OUTCOME_DRAW
	return OUTCOME_NONE

def make_random_move(state, player):
    col = np.random.choice(get_free_columns(state))
    return drop_piece(state, col, player)
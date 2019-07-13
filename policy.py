from board_utils import *
import numpy as np

def minimax(board, depth, alpha, beta, maximizing_player, curr_player):
	enemy = -1
	if curr_player == 1:
		enemy = 2
	else:
		enemy = 1
	free_cols = get_free_columns(board)
	is_terminal_node = check_terminal_node(board)
	if depth == 0 or is_terminal_node:
		if is_terminal_node:
			if check_for_winner(board, curr_player):
				return (None, 100)
			elif check_for_winner(board, enemy):
				return (None, -100)
			else:
				return (None, 0)
		else:
			return (None, score_position(board, curr_player))
	if maximizing_player:
		value = -math.inf
		column = np.random.choice(free_cols)
		for col in free_cols:
			temp_board = board.copy()
			drop_piece(temp_board, col, curr_player)
			new_score = minimax(temp_board, depth-1, alpha, beta, False, curr_player)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else:
		value = math.inf
		column = np.random.choice(free_cols)
		for col in free_cols:
			temp_board = board.copy()
			drop_piece(temp_board, col, enemy)
			new_score = minimax(temp_board, depth-1, alpha, beta, True, curr_player)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value
		
def random_block(board, curr_player):
	enemy = -1
	if curr_player == 2:
		enemy = 1
	else:
		enemy = 2
		
	free_cols = get_free_columns(board)
	for i in range(0, len(free_cols)):
		temp_board = board.copy()
		drop_piece(temp_board, free_cols[i], curr_player)
		if check_for_winner(temp_board, curr_player):
			return free_cols[i]
			
	for i in range(0, len(free_cols)):
		temp_board = board.copy()
		drop_piece(temp_board, free_cols[i], enemy)
		if check_for_winner(temp_board, enemy):
			return free_cols[i]
	
	return np.random.choice(free_cols)
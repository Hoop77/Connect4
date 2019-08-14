import numpy as np
import math
import board

# popular algorithm to solve board games, recursive search tree method
def minimax(state, depth, alpha, beta, maximizing_player, curr_player):
	enemy = -curr_player
	free_cols = board.get_free_columns(state)
	is_terminal_node = board.check_terminal_node(state)
	if depth == 0 or is_terminal_node:
		if is_terminal_node:
			if board.check_for_winner(state, curr_player):
				return None, math.inf
			elif board.check_for_winner(state, enemy):
				return None, -math.inf
			else:
				return None, 0
		else:
			return (None, board.score_position(state, curr_player))
	if maximizing_player:
		value = -math.inf
		column = np.random.choice(free_cols)
		for col in free_cols:
			temp_state = state.copy()
			board.drop_piece_inplace(temp_state, col, curr_player)
			new_score = minimax(temp_state, depth-1, alpha, beta, False, curr_player)[1]
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
			temp_state = state.copy()
			board.drop_piece_inplace(temp_state, col, enemy)
			new_score = minimax(temp_state, depth-1, alpha, beta, True, curr_player)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

# method looks one turn ahead
def random_block(state, curr_player):
	enemy = -curr_player
	free_cols = board.get_free_columns(state)
	for i in range(0, len(free_cols)):
		temp_state = state.copy()
		board.drop_piece_inplace(temp_state, free_cols[i], curr_player)
		if board.check_for_winner(temp_state, curr_player):
			return free_cols[i]
			
	for i in range(0, len(free_cols)):
		temp_state = state.copy()
		board.drop_piece_inplace(temp_state, free_cols[i], enemy)
		if board.check_for_winner(temp_state, enemy):
			return free_cols[i]
			
	return np.random.choice(free_cols)

# completly random choice of columns
def random_choice(state):
	return np.random.choice(board.get_free_columns(state))
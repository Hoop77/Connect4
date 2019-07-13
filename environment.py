import sys
import numpy as np
import math
import simplejson as json
from board_utils import drop_piece, check_for_winner, get_free_columns

NUM_BOARD_ROWS = 6
NUM_BOARD_COLS = 7

STATE_SHAPE = (NUM_BOARD_ROWS, NUM_BOARD_COLS)
NUM_ACTIONS = NUM_BOARD_COLS

FREE = 0
RED = 1
YELLOW = 2

WIN_REWARD = 1
LOST_REWARD = -1
DRAW_REWARD = 0.25 # TODO try out

class Environment:
	def __init__(self, opponent_policy, agent_color=RED, agent_first_turn=True):
		self.board = np.zeros(STATE_SHAPE)
		self.opponent_policy = opponent_policy
		self.agent_color = agent_color
		self.opponent_color = RED if agent_color is YELLOW else YELLOW
		self.agent_first_turn = agent_first_turn

	def get_state(self):
		return self.board

	def step(self, action):
		next_state = None
		reward = 0
		done = False

		if self.agent_first_turn:
			drop_piece(self.board, action, self.agent_color)
			if check_for_winner(self.board, self.agent_color):
				reward = WIN_REWARD
				done = True
			elif len(get_free_columns(self.board)) == 0: # draw
				reward = DRAW_REWARD
				done = True
			else:
				opponent_action = self.opponent_policy(self.board)
				drop_piece(self.board, opponent_action, self.opponent_color)
				if check_for_winner(self.board, self.opponent_color):
					reward = LOST_REWARD
					done = True
				elif len(get_free_columns(self.board)) == 0: # draw
					reward = DRAW_REWARD
					done = True
				else:
					next_state = self.board.copy()
		else:
			opponent_action = self.opponent_policy(self.board)
			drop_piece(self.board, opponent_action, self.opponent_color)
			if check_for_winner(self.board, self.opponent_color):
				reward = LOST_REWARD
				done = True
			elif len(get_free_columns(self.board)) == 0: # draw
				reward = DRAW_REWARD
				done = True
			else:
				drop_piece(self.board, action, self.agent_color)
				if check_for_winner(self.board, self.agent_color):
					reward = WIN_REWARD
					done = True
				elif len(get_free_columns(self.board)) == 0: # draw
					reward = DRAW_REWARD
					done = True
				else:
					next_state = self.board.copy()

		return next_state, reward, done
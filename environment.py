import sys
import numpy as np
import math
import simplejson as json
import board

class Environment:
	def __init__(self, opponent_policy, agent_color=board.RED, agent_first_turn=True):
		self.state = np.zeros(board.STATE_SHAPE)
		self.opponent_policy = opponent_policy
		self.agent_color = agent_color
		self.opponent_color = board.RED if agent_color is board.YELLOW else board.YELLOW
		self.agent_first_turn = agent_first_turn

	def get_state(self):
		return self.state

	def step(self, action):
		reward = 0
		done = False
		if self.agent_first_turn:
			board.drop_piece(self.state, action, self.agent_color)
			if board.check_for_winner(self.state, self.agent_color):
				reward = board.REWARD_WIN
				done = True
			elif len(board.get_free_columns(self.state)) == 0: # draw
				reward = board.REWARD_DRAW
				done = True
			else:
				opponent_action = self.opponent_policy(self.state)
				board.drop_piece(self.state, opponent_action, self.opponent_color)
				if board.check_for_winner(self.state, self.opponent_color):
					reward = board.REWARD_DEFEAT
					done = True
				elif len(board.get_free_columns(self.state)) == 0: # draw
					reward = board.REWARD_DRAW
					done = True
		else:
			opponent_action = self.opponent_policy(self.state)
			board.drop_piece(self.state, opponent_action, self.opponent_color)
			if board.check_for_winner(self.state, self.opponent_color):
				reward = board.REWARD_DEFEAT
				done = True
			elif len(board.get_free_columns(self.state)) == 0: # draw
				reward = board.REWARD_DRAW
				done = True
			else:
				board.drop_piece(self.state, action, self.agent_color)
				if board.check_for_winner(self.state, self.agent_color):
					reward = board.REWARD_WIN
					done = True
				elif len(board.get_free_columns(self.state)) == 0: # draw
					reward = board.REWARD_DRAW
					done = True

		next_state = self.state.copy()
		return next_state, reward, done
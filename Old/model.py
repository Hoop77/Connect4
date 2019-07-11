import sys
import random
import numpy as np
import math
from policy import *

BOARD_ROWS = 6
BOARD_COLS = 7

EMPTY = 0
PLAYER_ONE = 1
PLAYER_TWO = 2

# https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py
# http://blog.gamesolver.org/

# global
isGameOver = False
isPlayerOne = True

class Environment:
	def __init__(self):
		self.board = np.zeros((6, 7))

	def getState(self):
		return self.board
		
	def setState(self, state):
		self.board = state

	def dropCoin(self, col):
		if is_valid_location(self.board, col):
			row = get_next_open_row(self.board, col)
			drop_piece(self.board, row, col, 2)

class Agent:
	def __init__(self, env):
		self.total_reward = 0.0
		self.env = env

	def humanAction(self, col):
		global isGameOver
		board = self.env.getState()
		if is_valid_location(board, col):
			row = get_next_open_row(board, col)
			if isPlayerOne:
				drop_piece(board, row, col, PLAYER_ONE)
			else:
				drop_piece(board, row, col, PLAYER_TWO)

		if winning_move(board, PLAYER_PIECE):
			isGameOver = True

	def action(self,currPlayer):
		global isGameOver
		board = self.env.getState()
		
		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True, currPlayer)
		print("score", minimax_score)
		
		# print("Col: ", col, "Score: ", minimax_score)
		#if is_valid_location(board, col):
		#	row = get_next_open_row(board, col)
		#	if isPlayerOne:
		#		drop_piece(board, row, col, PLAYER_ONE)
		#	else:
		#		drop_piece(board, row, col, PLAYER_TWO)

		#if winning_move(board, PLAYER_PIECE):
		#	isGameOver = True
		
		#col = randomBlock(board, currPlayer)
			
		return col


import numpy as np
import random
import pygame
import sys
import math

BOARD_ROWS = 6
BOARD_COLS = 7

WINDOW_LENGTH = 4

def minimax(board, depth, alpha, beta, maximizingPlayer, currPlayer):
	enemy = -1
	if currPlayer == 1:
		enemy = 2
	else:
		enemy = 1
	freeCols = getFreeColumns(board)
	isTerminalNode = checkTerminalNode(board)
	if depth == 0 or isTerminalNode:
		if isTerminalNode:
			if checkForWinner(board, currPlayer):
				return (None, 100)
			elif checkForWinner(board, enemy):
				return (None, -100)
			else:
				return (None, 0)
		else:
			return (None, score_position(board, currPlayer))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(freeCols)
		for col in freeCols:
			tempBoard = board.copy()
			dropPiece(tempBoard, col, currPlayer)
			new_score = minimax(tempBoard, depth-1, alpha, beta, False, currPlayer)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else:
		value = math.inf
		column = random.choice(freeCols)
		for col in freeCols:
			tempBoard = board.copy()
			dropPiece(tempBoard, col, enemy)
			new_score = minimax(tempBoard, depth-1, alpha, beta, True, currPlayer)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value
		
def randomBlock(board, currPlayer):
	enemy = -1
	if currPlayer == 2:
		enemy = 1
	else:
		enemy = 2
		
	freeCols = getFreeColumns(board);
	for i in range(0, len(freeCols)):
		tempBoard = board.copy()
		dropPiece(tempBoard, freeCols[i], currPlayer)
		if checkForWinner(tempBoard, currPlayer):
			return freeCols[i]
			
	for i in range(0, len(freeCols)):
		tempBoard = board.copy()
		dropPiece(tempBoard, freeCols[i], enemy)
		if checkForWinner(tempBoard, enemy):
			return freeCols[i]
	
	return random.choice(freeCols)
		
def dropPiece(board, col, player):
	for row in range(0, BOARD_ROWS):
		if board[row][col] != 0:
			board[row-1][col] = player
			break
		if row == 5 and board[row][col] == 0:
			board[row][col] = player
	
def getFreeColumns(board):
	freeCols = []
	for col in range(0, BOARD_COLS):
		if board[0][col] == 0:
			freeCols.append(col)
	return freeCols
	
def checkForWinner(board, player):
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
	
def checkTerminalNode(board):
	return checkForWinner(board, 1) or checkForWinner(board, 2) or len(getFreeColumns(board)) == 0
	
def evaluateSection(toEvaluate, currPlayer):

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

	return score

def score_position(board, currPlayer):

	print("board", board.shape)
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, BOARD_COLS//2])]
	center_count = center_array.count(currPlayer)
	score += center_count * 3

	# score horizontal spaces			
	for x in range(0, 6):
		for y in range(0, 4):
			toEvaluate = [int(i) for i in list(board[x][y:y+3])]
			print("HORIZONTAL",toEvaluate)
			score += evaluateSection(toEvaluate, currPlayer)

	# score vertical spaces
	for x in range(0, 3):
		for y in range(0, 7):
			toEvaluate = [int(i) for i in list(board[x:x+3][y])]
			print("vertical",toEvaluate)
			score += evaluateSection(toEvaluate, currPlayer)

	# score / diagonal spaces
	for x in range(0, 3):
		for y in range(3, 7):
			toEvaluate = [int(i) for i in list(board[x:x+3][y:y-3])]
			print("diagonal1",toEvaluate)
			score += evaluateSection(toEvaluate, currPlayer)

	# score \ diagonal spaces
	for x in range(0, 3):
		for y in range(0, 4):
			toEvaluate = [int(i) for i in list(board[x:x+3][y:y+3])]
			print("diagonal2",toEvaluate)
			score += evaluateSection(toEvaluate, currPlayer)

	return score
			
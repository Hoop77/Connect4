import board
import numpy as np

def evaluate(agent, graph, session):
    player1_counter = 0
    player2_counter = 0
    tie_counter = 0
    episodes = 1000
    while(episodes != 0):
        state = np.zeros((6,7))
        end = True
        while end:
            board.make_random_move(state, board.PLAYER_1)
            if board.check_for_winner(state, board.PLAYER_1):
                player1_counter = player1_counter + 1
                end = False
                break

            with graph.as_default():
                with session.as_default():
                    agent.load('models/model.h5')
                    col, free_cols, col_values = agent.act(state, board.PLAYER_2)
                    state = board.drop_piece(state,col,board.PLAYER_2)
            if board.check_for_winner(state, board.PLAYER_2):
                player2_counter = player2_counter + 1
                end = False
                break
            
            if len(board.get_free_columns(state)) == 0:
                tie_counter = tie_counter + 1
                end = False
                break

        episodes = episodes - 1

    print("player1_counter", player1_counter)
    print("player2_counter", player2_counter)
    print("tie_counter", tie_counter)
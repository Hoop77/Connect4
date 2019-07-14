from environment import Environment
import board
import numpy as np

def test_step():
    env = Environment(opponent_policy=lambda s: 0)
    next_state, reward, done = env.step(1)
    next_state, reward, done = env.step(1)
    next_state, reward, done = env.step(1)
    next_state, reward, done = env.step(2)
    if reward != board.REWARD_DEFEAT or done is not True:
        print('FAIL')

if __name__ == '__main__':
    test_step()
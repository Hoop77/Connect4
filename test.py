from environment import Environment
import board
import numpy as np
from agent import DQNAgent

def test_step():
    env = Environment(opponent_policy=lambda s: 0)
    next_state, reward, done = env.step(1)
    next_state, reward, done = env.step(1)
    next_state, reward, done = env.step(1)
    next_state, reward, done = env.step(2)
    if reward != board.REWARD_DEFEAT or done is not True:
        print('FAIL')

def test_target_model():
    agent = DQNAgent()
    agent.load('models/model.h5')
    state = np.zeros([6, 7])
    state[5][3] = 1
    state = state.reshape(1, 6, 7, 1)
    p1 = agent.policy_model.predict(state)
    p2 = agent.target_model.predict(state)
    print(p1)
    print(p2)
    if not np.array_equal(p1, p2):
        print('FAIL')

if __name__ == '__main__':
    test_target_model()
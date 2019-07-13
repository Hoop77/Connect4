from agent import DQNAgent
from environment import Environment
from policy import minimax
import math
import board
import statistics

def train(model_path, **params): 
    agent = DQNAgent(**params)
    for e in range(params['num_episodes']):
        print('Episode {}/{}'.format(e, params['num_episodes']))
        env = Environment(opponent_policy=params['opponent_policy'], agent_color=board.RED, agent_first_turn=True)
        done = False
        while not done:
            state = env.get_state()
            action = agent.act_epsilon_greedy(state)
            next_state, reward, done = env.step(action)
            if reward == board.WIN_REWARD:
                print("Won Game!")
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
    agent.save(model_path)
from agent import DQNAgent
from environment import Environment
from policy import minimax
import math
import board
import statistics
import time

def train(model_path, **params): 
    stats = statistics.default_stats()
    agent = DQNAgent(**params)
    for e in range(params['num_episodes']):
        print('Episode {}/{}'.format(e, params['num_episodes']))
        env = Environment(opponent_policy=params['opponent_policy'], agent_color=board.RED, agent_first_turn=True)
        done = False
        while not done:
            state = env.get_state()
            action = agent.act_epsilon_greedy(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.replay(stats=stats)

            if reward == board.WIN_REWARD:
                print("Won Game!")
                stats['num_wins'] += 1
            elif reward == board.DEFEAT_REWARD:
                stats['num_defeats'] += 1
            elif reward == board.DRAW_REWARD:
                stats['num_draws'] += 1                

    agent.save(model_path)
    statistics.save_stats(stats, params, "stats/stats-{}.json".format(time.strftime("%Y%m%d-%H%M%S")))
    statistics.show_stats(stats)
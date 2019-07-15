from agent import DQNAgent
from environment import Environment
from policy import minimax, random_choice
import math
import board
import statistics
import time
from matplotlib import pyplot as plt

def train(model_path='models/model.h5', 
          opponent_policy=random_choice,
          num_episodes=1000,
          agent_params={},
          **kwargs):
    stats = statistics.default_stats()
    plt_data = statistics.plot_stats(stats, data=None)

    agent = DQNAgent(**agent_params)

    for episode in range(num_episodes):
        print('Episode {}/{}'.format(episode, num_episodes))
        env = Environment(opponent_policy=opponent_policy, agent_color=board.RED, agent_first_turn=True)
        done = False
        episode_length = 0
        while not done:
            state = env.get_state()
            action = agent.act_epsilon_greedy(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.replay(stats=stats)

            if reward == board.REWARD_WIN:
                print("Won Game!")
                stats['num_wins'] += 1
            elif reward == board.REWARD_DEFEAT:
                stats['num_defeats'] += 1
            elif reward == board.REWARD_DRAW:
                stats['num_draws'] += 1
            
            episode_length += 1

        stats['episode_lengths'].append(episode_length)

        plt_data = statistics.plot_stats(stats, data=plt_data)
        plt.pause(0.0001)

        if episode % 100 == 0:
            agent.save(model_path)

    agent.save(model_path)
    saved_params = {
        'agent_params': agent_params,
        'num_episodes': num_episodes
    }
    statistics.save_stats(stats, saved_params, "stats/stats-{}.json".format(time.strftime("%Y%m%d-%H%M%S")))
    statistics.plot_stats(stats, data=plt_data)
    plt.show()
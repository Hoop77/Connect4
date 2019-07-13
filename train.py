from agent import DQNAgent
from environment import Environment
from policy import minimax, random_choice
import math
import board
import statistics
import time

def train(model_path, 
          opponent_policy=random_choice,
          num_episodes=1000,
          agent_params={},
          **kwargs):
    stats = statistics.default_stats()
    agent = DQNAgent(agent_params)
    for e in range(num_episodes):
        print('Episode {}/{}'.format(e, num_episodes))
        env = Environment(opponent_policy=opponent_policy, agent_color=board.RED, agent_first_turn=True)
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

    agent.save('models/model.h5')
    saved_params = {
        'agent_params': agent_params,
        'num_episodes': num_episodes
    }
    statistics.save_stats(stats, saved_params, "stats/stats-{}.json".format(time.strftime("%Y%m%d-%H%M%S")))
    statistics.show_stats(stats)
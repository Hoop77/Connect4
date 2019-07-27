import numpy as np
np.random.seed(0)
from agent import Agent
from policy import minimax, random_choice
import math
import board
import statistics
import time
import datetime
from matplotlib import pyplot as plt

def train(model_path='models/model.h5', 
          resume_training=False,
          num_episodes=1000,
          life_plot=True,
          self_play_args={},
          agent_args={},
          **kwargs):
    stats = statistics.default_stats()
    stats_filename = "stats/stats-{}.json".format(time.strftime("%Y%m%d-%H%M%S"))
    plt_data = statistics.plot_stats(stats, data=None)

    agent = Agent(**agent_args)
    if resume_training:
        agent.load(model_path)

    for episode in range(num_episodes):
        print('Episode {}/{}'.format(episode, num_episodes))       

        agent.self_play(stats=stats, **self_play_args)

        if life_plot:
            plt_data = statistics.plot_stats(stats, data=plt_data)
            plt.pause(0.0001)

        if episode % 100 == 0:
            agent.save(model_path)
            # TODO: fixit
            # saved_args = {
            #     'agent_args': agent_args,
            #     'num_episodes': num_episodes
            # }
            # statistics.save_stats(stats, saved_args, stats_filename)
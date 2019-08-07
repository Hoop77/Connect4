import numpy as np
np.random.seed(0)
from agent import Agent
from policy import minimax, random_choice
import board
import datetime
from matplotlib import pyplot as plt
from statistics import show_life_plot, get_life_plot_stats

def train(stats=None, file_name='models/model.h5', 
          resume_training=False,
          num_episodes=1000,
          life_plot=True,
          create_stats=True,
          agent_args={},
          **kwargs):

    life_plot_stats = get_life_plot_stats()
    plt_data = show_life_plot(life_plot_stats, data=None)

    agent = Agent(num_episodes, **agent_args)
    if resume_training:
        agent.load(file_name)

    for episode in range(num_episodes + 1):
        print('Episode {}/{}'.format(episode, num_episodes))

        loss, epsilon, learning_rate = agent.self_play()

        if create_stats and episode % 25 == 0:
            stats.append_stats("<episode="+str(episode)+">")
            stats.append_stats("<loss="+np.format_float_positional((np.round(np.float32(loss),6)))+">")
            stats.append_stats("<epsilon="+np.format_float_positional((np.round(np.float32(epsilon),6)))+">")
            stats.append_stats("<learning_rate="+np.format_float_positional((np.round(np.float32(learning_rate),6)))+">")

        if life_plot and episode % 25 == 0:
            life_plot_stats['episode'].append(episode)
            life_plot_stats['loss'].append(loss)
            life_plot_stats['epsilon'].append(epsilon)
            life_plot_stats['learning_rate'].append(learning_rate)
            plt_data = show_life_plot(life_plot_stats, data=plt_data)
            plt.pause(0.0001)

        if episode % 100 == 0:
            agent.save(file_name)

        if episode % 50000 == 0:
            model_path = "models/model"+str(episode)+".h5"
            agent.save(model_path)
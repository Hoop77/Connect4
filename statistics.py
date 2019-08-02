from matplotlib import pyplot as plt
import json
import time
from collections import deque
import re
import numpy as np

class Stats:
    def __init__(self, args=None):
        if args is not None:
            self.file_name = "stats/stats-{}.txt".format(time.strftime("%d.%m.%Y-%H%M%S"))
            self.create_stats_file(json.dumps(args))

    def create_stats_file(self, data):
        f = open(self.file_name, "w")
        f.write(data)
        f.close()

    def append_stats(self, data):
        f = open(self.file_name, "a")
        f.write(data)
        f.close()

    def plot_stats(self, file_name):
        episode_pattern = re.compile("<(episode=)([0-9\.]*)>")
        loss_pattern = re.compile("<(loss=)([0-9\.]*)>")
        epsilon_pattern = re.compile("<(epsilon=)([0-9\.]*)>")
        learning_rate_pattern = re.compile("<(learning_rate=)([0-9\.]*)>")

        f = open(file_name, "r")
        file_content = f.read()
        f.close()

        temp_episode_matches = re.findall(episode_pattern, file_content)
        temp_loss_matches = re.findall(loss_pattern, file_content)
        temp_epsilon_matches = re.findall(epsilon_pattern, file_content)
        temp_learning_rate_matches = re.findall(learning_rate_pattern, file_content)

        episode_matches = []
        loss_matches = []
        epsilon_matches = []
        learning_rate_matches = []

        for match in temp_episode_matches:
            episode_matches.append(float(match[1]))
        for match in temp_loss_matches:
            loss_matches.append(float(match[1]))
        for match in temp_epsilon_matches:
            epsilon_matches.append(float(match[1]))
        for match in temp_learning_rate_matches:
            learning_rate_matches.append(float(match[1]))

        plt.subplot(3, 1, 1)
        plt.plot(np.array(episode_matches), np.array(loss_matches))
        plt.xlabel('Episodes')
        plt.ylabel('Loss')

        plt.subplot(3, 1, 2)
        plt.plot(np.array(episode_matches), np.array(epsilon_matches))
        plt.xlabel('Episodes')
        plt.ylabel('Epsilon')

        plt.subplot(3, 1, 3)
        plt.plot(np.array(episode_matches), np.array(learning_rate_matches))
        plt.xlabel('Episodes')
        plt.ylabel('Learning rate')

        plt.tight_layout()

        plt.show()

def get_life_plot_stats():
    return {
        'episode': deque(maxlen=500),
        'loss': deque(maxlen=500),
        'epsilon': deque(maxlen=500),
        'learning_rate': deque(maxlen=500)
    }

def show_life_plot(stats, data=None):
    if data is None:
        fig, axes = plt.subplots(3)
    else:
        fig, axes = data[0], data[1]
        for ax in axes:
            ax.clear()

    axes[0].plot(list(stats['episode']), list(stats['loss']))
    axes[0].set_xlabel('episode')
    axes[0].set_ylabel('loss')
    
    axes[1].plot(list(stats['episode']), list(stats['epsilon']))
    axes[1].set_xlabel('episode')
    axes[1].set_ylabel('epsilon')

    axes[2].plot(list(stats['episode']), list(stats['learning_rate']))
    axes[2].set_xlabel('episode step')
    axes[2].set_ylabel('leraning_rate')

    return (fig, axes)


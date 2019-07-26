from matplotlib import pyplot as plt
import json
import copy
import board
from collections import deque

# TODO: make it a class

def default_stats():
    return {
        'episode_outcomes': deque(maxlen=100),
        'episode_lengths': deque(maxlen=100),
        'loss': {'steps': [deque(maxlen=100)], 'values': [deque(maxlen=100)]}
    }

def save_stats(stats, params, path):
    with open(path, 'w') as f:
        f.write(json.dumps({'params': params, 'stats': stats}))

def load_stats(path):
    with open(path, 'r') as f:
        j = json.load(f)
        return j['stats'], j['params'] 

def plot_stats(stats, data=None):
    if data is None:
        fig, axes = plt.subplots(3)
    else:
        fig, axes = data[0], data[1]
        for ax in axes:
            ax.clear()

    episode_outcomes = list(stats['episode_outcomes'])
    num_wins_player_1 = episode_outcomes.count(board.PLAYER_1)
    num_wins_player_2 = episode_outcomes.count(board.PLAYER_2)
    num_draws = episode_outcomes.count(0)

    axes[0].pie([num_wins_player_1, num_wins_player_2, num_draws], labels=['wins player 1', 'wins player 2', 'draws'])
    
    axes[1].plot(list(stats['episode_lengths']))
    axes[1].set_xlabel('episode')
    axes[1].set_ylabel('episode length')

    axes[2].plot(list(stats['loss']['steps']), list(stats['loss']['values']))
    axes[2].set_xlabel('training step')
    axes[2].set_ylabel('loss')

    return (fig, axes)

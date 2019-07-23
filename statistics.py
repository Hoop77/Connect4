from matplotlib import pyplot as plt
import json
import copy
import board

def default_stats():
    return {
        'episode_outcomes': [],
        'episode_lengths': [],
        'epsilon': {'steps': [], 'values': []},
        'loss': {'steps': [], 'values': []}
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
        fig, axes = plt.subplots(4)
    else:
        fig, axes = data[0], data[1]
        for ax in axes:
            ax.clear()

    episode_results = stats['episode_outcomes'][-100:]
    num_wins_player_1 = episode_results.count(board.PLAYER_1)
    num_wins_player_2 = episode_results.count(board.PLAYER_2)
    num_draws = episode_results.count(0)

    axes[0].pie([num_wins_player_1, num_wins_player_2, num_draws], labels=['wins player 1', 'wins player 2', 'draws'])
    
    axes[1].plot(stats['episode_lengths'])
    axes[1].set_xlabel('episode')
    axes[1].set_ylabel('episode length')

    axes[2].plot(stats['epsilon']['steps'], stats['epsilon']['values'])
    axes[2].set_xlabel('training step')
    axes[2].set_ylabel('epsilon')
    axes[2].set_ylim(0, 1)

    axes[3].plot(stats['loss']['steps'], stats['loss']['values'])
    axes[3].set_xlabel('training step')
    axes[3].set_ylabel('loss')

    return (fig, axes)

from matplotlib import pyplot as plt
import json
import copy

def default_stats():
    return {
        'num_wins': 0,
        'num_defeats': 0,
        'num_draws': 0,
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

    axes[0].pie([stats['num_wins'], stats['num_defeats'], stats['num_draws']], labels=['win', 'defeat', 'draw'])
    
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

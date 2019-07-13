from matplotlib import pyplot as plt
import json
import copy

def default_stats():
    return {
        'num_wins': 0,
        'num_defeats': 0,
        'num_draws': 0,
        'loss': {'steps': [], 'values': []},
        'accuracy': {'steps': [], 'values': []},
    }

def save_stats(stats, params, path):
    with open(path, 'w') as f:
        f.write(json.dumps({'params': params, 'stats': stats}))

def load_stats(path):
    with open(path, 'r') as f:
        j = json.load(f)
        return j['stats'], j['params']

def show_stats(stats):
    fig, axes = plt.subplots(3)
    axes[0].pie([stats['num_wins'], stats['num_defeats'], stats['num_draws']], labels=['win', 'defeat', 'draw'])
    axes[1].plot(stats['loss']['steps'], stats['loss']['values'])
    axes[1].set_xlabel('t')
    axes[1].set_ylabel('loss')
    axes[2].plot(stats['accuracy']['steps'], stats['accuracy']['values'])
    axes[2].set_xlabel('t')
    axes[2].set_ylabel('accuracy')
    plt.show()
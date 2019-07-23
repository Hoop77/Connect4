from agent import Agent
from policy import minimax, random_choice
import math
import board
import statistics
import time
from matplotlib import pyplot as plt
import numpy as np

REWARD_TABLE = {
	board.OUTCOME_NONE: 0.0,
	board.OUTCOME_WIN: 1.0,
	board.OUTCOME_DEFEAT: 0.0,
	board.OUTCOME_DRAW: 0.5
}

def train(model_path='models/model.h5', 
          opponent_policy=random_choice,
          num_episodes=1000,
          self_play_args={},
          agent_args={},
          **kwargs):
    stats = statistics.default_stats()
    plt_data = statistics.plot_stats(stats, data=None)

    agent = Agent(**agent_args)

    for episode in range(num_episodes):
        print('Episode {}/{}'.format(episode, num_episodes))       

        self_play(agent, stats=stats, **self_play_args)

        plt_data = statistics.plot_stats(stats, data=plt_data)
        plt.pause(0.0001)

        if episode % 100 == 0:
            agent.save(model_path)

    agent.save(model_path)
    saved_args = {
        'agent_args': agent_args,
        'num_episodes': num_episodes
    }
    statistics.save_stats(stats, saved_args, "stats/stats-{}.json".format(time.strftime("%Y%m%d-%H%M%S")))
    statistics.plot_stats(stats, data=plt_data)
    plt.show()

def self_play(agent, 
              epsilon=0.1,
              gamma=0.9,
              stats=None):
    episode_length = 0
    state = np.zeros(board.STATE_SHAPE)
    player = board.PLAYER_1
    outcome = board.OUTCOME_NONE
    while outcome == board.OUTCOME_NONE:
        is_random_move = np.random.rand() <= epsilon
        if is_random_move:
            next_state = random_move(state, player)
            outcome = board.get_outcome_after_move(next_state, player)
            if outcome == board.OUTCOME_WIN:
                target = REWARD_TABLE[outcome]
                agent.train(state, target, stats=stats)
        else:
            next_state, target = choose_move(agent, state, player, gamma)
            agent.train(state, target, stats=stats)

        outcome = board.get_outcome_after_move(next_state, player)
        state = next_state
        player = -player
        episode_length += 1
    
    stats['episode_outcomes'].append(-player)
    stats['episode_lengths'].append(episode_length)

def random_move(state, player):
    col = np.random.choice(board.get_free_columns(state))
    return board.drop_piece(state, col, player)

def choose_move(agent, state, player, gamma):
    cols = board.get_free_columns(state)
    next_states = [board.drop_piece(state, col, player) for col in cols]
    outcomes = [board.get_outcome_after_move(next_state, player) for next_state in next_states]
    rewards = np.array([REWARD_TABLE[outcome] for outcome in outcomes])
    not_done = np.array([outcome == board.OUTCOME_NONE for outcome in outcomes]).astype(np.float32)
    values = np.array([agent.evaluate(next_state, use_target_model=True) for next_state in next_states])
    targets = rewards + not_done * gamma * values # TODO fixit
    targets = np.round(targets, 5)
    targets = player * targets
    target_max = np.max(targets)
    best_next_states = [next_states[i] for i, target in enumerate(targets) if target == target_max]
    idx = np.random.choice(len(best_next_states))
    best_next_state = best_next_states[idx]
    return best_next_state, player * target_max
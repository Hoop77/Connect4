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

REWARD_TABLE = {
	board.OUTCOME_NONE: 0.0,
	board.OUTCOME_WIN: 1.0,
	board.OUTCOME_DEFEAT: -1.0,
	board.OUTCOME_DRAW: 0.5
}

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

        self_play(agent, stats=stats, **self_play_args)

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

def self_play(agent,
              epsilon=0.1,
              gamma=0.9,
              stats=None):
    episode_length = 0
    state = np.zeros(board.STATE_SHAPE)
    player = board.PLAYER_1
    outcome = board.OUTCOME_NONE
    while outcome == board.OUTCOME_NONE:
        random_move = np.random.rand() <= epsilon
        if random_move:
            next_state = make_random_move(state, player)
            outcome = board.get_outcome_after_move(next_state, player)
            if outcome == board.OUTCOME_WIN or outcome == board.OUTCOME_DEFEAT:
                target = REWARD_TABLE[outcome]
                agent.train(state, target, stats=stats)
        else:
            next_state, target = make_best_move(agent, state, player, gamma)
            agent.train(state, target, stats=stats)

        outcome = board.get_outcome_after_move(next_state, player)
        state = next_state
        player = -player
        episode_length += 1
    
    stats['episode_outcomes'].append(-player)
    stats['episode_lengths'].append(episode_length)

def make_random_move(state, player):
    col = np.random.choice(board.get_free_columns(state))
    return board.drop_piece(state, col, player)

def make_best_move(agent, state, player, gamma):
    cols = board.get_free_columns(state)
    next_states = [board.drop_piece(state, col, player) for col in cols]
    outcomes = [board.get_outcome_after_move(next_state, player) for next_state in next_states]
    rewards = np.array([REWARD_TABLE[outcome] for outcome in outcomes])
    not_done = np.array([outcome == board.OUTCOME_NONE for outcome in outcomes]).astype(np.float32)
    values = np.squeeze(agent.model.predict(np.expand_dims(next_states, axis=3)))
    targets = rewards + not_done * gamma * values
    targets = player * targets
    target_max_idx = np.argmax(targets)
    target_max = targets[target_max_idx]
    best_next_state = next_states[target_max_idx]
    return best_next_state, player * target_max
# -*- coding: utf-8 -*-
import numpy as np
from collections import deque
from keras.models import Sequential, clone_model
from keras.layers import Dense, Conv2D, LeakyReLU, Flatten
import board
import math
import random
random.seed(0)

class DQNAgent:
    def __init__(self, 
                 weights=None,
                 memory_size=2000, 
                 gamma=0.95,
                 epsilon=1.0,
                 epsilon_min=0.01,
                 epsilon_decay=0.995,
                 batch_size=32,
                 update_interval=100,
                 num_epochs=5,
                 **kwargs):
        self.memory = deque(maxlen=memory_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.policy_model = self.build_model()
        self.target_model = None
        self.update_target_model()
        self.update_interval = update_interval
        self.total_steps = 0
        self.num_epochs = num_epochs

    def act(self, state):
        Q_state = self.predict(state)
        return board.choose_best_action(state, Q_state)
    
    def act_epsilon_greedy(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(board.get_free_columns(state))
        return self.act(state)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, stats=None):
        if len(self.memory) < self.batch_size:
            return

        if self.total_steps % self.update_interval == 0:
            self.update_target_model()

        minibatch = random.sample(self.memory, self.batch_size)
        states_batch, action_batch, reward_batch, next_states_batch, done_batch = map(np.array, zip(*minibatch))
        states_batch = states_batch.reshape(len(states_batch), board.NUM_ROWS, board.NUM_COLS, 1)
        next_states_batch = next_states_batch.reshape(len(next_states_batch), board.NUM_ROWS, board.NUM_COLS, 1)
        targets_batch = np.zeros([self.batch_size, board.NUM_ACTIONS])
        Q_state_batch = self.policy_model.predict(states_batch)
        Q_next_state_batch = self.policy_model.predict(next_states_batch)
        Q_next_state_target_batch = self.target_model.predict(next_states_batch)
        i = 0
        for state, action, reward, next_state, done in minibatch:
            Q_state = Q_state_batch[i]
            Q_next_state = Q_next_state_batch[i]
            Q_next_state_target = Q_next_state_target_batch[i]
            target = reward
            if not done:
                best_action = board.choose_best_action(next_state, Q_next_state)
                target = reward + self.gamma * Q_next_state_target[best_action]
            targets_batch[i] = Q_state
            targets_batch[i][action] = target
            i += 1

        self.policy_model.fit(states_batch, targets_batch, epochs=self.num_epochs, verbose=0)

        if stats is not None and self.total_steps % 100 == 0:
            result = self.policy_model.evaluate(states_batch, targets_batch, verbose=0)
            stats['loss']['steps'].append(self.total_steps)
            stats['loss']['values'].append(result[0])
            stats['accuracy']['steps'].append(self.total_steps)
            stats['accuracy']['values'].append(result[1])

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        self.total_steps += 1

    def load(self, path):
        self.policy_model.load_weights(path)

    def save(self, path):
        self.policy_model.save_weights(path)

    def build_model(self):
        input_shape = (board.NUM_ROWS, board.NUM_COLS, 1)
        model = Sequential()
        model.add(Conv2D(30, (4, 4), padding='same', input_shape=input_shape))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(30, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(30, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Flatten())
        model.add(Dense(50, activation='linear'))
        model.add(Dense(board.NUM_COLS, activation='linear'))

        self.compile_model(model)

        # model.summary()
        return model
    
    def update_target_model(self):
        self.target_model = clone_model(self.policy_model)
        self.compile_model(self.target_model)
        self.target_model.set_weights(self.policy_model.get_weights())
    
    def compile_model(self, model):
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

    def predict(self, state):
        state = state.reshape(1, board.NUM_ROWS, board.NUM_COLS, 1)
        return self.policy_model.predict(state)[0]
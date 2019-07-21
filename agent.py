# -*- coding: utf-8 -*-
import numpy as np
from collections import deque
from keras.models import Sequential, clone_model
from keras.layers import Dense, Conv2D, LeakyReLU, Flatten
from keras.optimizers import Adam
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
                 update_interval=10,
                 num_epochs=5,
                 learning_rate=0.001,
                 **kwargs):
        self.memory = deque(maxlen=memory_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.learning_rate = learning_rate
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
        self.memory.append(np.array([state, action, reward, next_state, done]))

    def replay(self, stats=None):
        if len(self.memory) < self.batch_size:
            return

        if self.total_steps % self.update_interval == 0:
            self.update_target_model()

        minibatch = random.sample(self.memory, self.batch_size)
        state_batch = np.array([item[0] for item in minibatch]).reshape(self.batch_size, board.NUM_ROWS, board.NUM_COLS, 1)
        next_state_batch = np.array([item[3] for item in minibatch]).reshape(self.batch_size, board.NUM_ROWS, board.NUM_COLS, 1)
        target_batch = self.policy_model.predict(state_batch)
        Q_next_state_policy_batch = self.policy_model.predict(next_state_batch)
        Q_next_state_target_batch = self.target_model.predict(next_state_batch)
        i = 0
        for state, action, reward, next_state, done in minibatch:
            Q_next_state_policy = Q_next_state_policy_batch[i]
            Q_next_state_target = Q_next_state_target_batch[i]
            target = reward
            if not done:
                best_action = board.choose_best_action(next_state, Q_next_state_policy)
                target = reward + self.gamma * Q_next_state_target[best_action]
            target_batch[i][action] = target
            i += 1

        history = self.policy_model.fit(state_batch, target_batch, epochs=self.num_epochs, verbose=0)

        stats['loss']['steps'].append(self.total_steps)
        stats['loss']['values'].append(np.sqrt(history.history['loss'][-1]))
        
        stats['epsilon']['steps'].append(self.total_steps)
        stats['epsilon']['values'].append(self.epsilon)
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
        
        self.total_steps += 1

    def load(self, path):
        self.policy_model.load_weights(path)
        self.update_target_model()

    def save(self, path):
        self.policy_model.save_weights(path)

    def build_model(self):
        input_shape = (board.NUM_ROWS, board.NUM_COLS, 1)
        model = Sequential()
        model.add(Conv2D(32, (4, 4), padding='same', input_shape=input_shape))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(32, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Flatten())
        model.add(Dense(50))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Dense(board.NUM_COLS, activation='linear'))

        self.compile_model(model)

        return model
    
    def update_target_model(self):
        self.target_model = clone_model(self.policy_model)
        self.compile_model(self.target_model)
        self.target_model.set_weights(self.policy_model.get_weights())
    
    def compile_model(self, model):
        model.compile(optimizer=Adam(lr=self.learning_rate), loss='mean_squared_error')

    def predict(self, state):
        state = state.reshape(1, board.NUM_ROWS, board.NUM_COLS, 1)
        return self.policy_model.predict(state)[0]
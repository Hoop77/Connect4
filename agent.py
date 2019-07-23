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

class Agent:
    def __init__(self, 
                 weights=None,
                 gamma=0.95,
                 update_interval=10,
                 num_epochs=5,
                 learning_rate=0.001,
                 **kwargs):
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.model = self.build_model()
        self.target_model = None
        self.update_target_model()
        self.update_interval = update_interval
        self.total_steps = 0
        self.num_epochs = num_epochs

    def act(self, state, player):
        cols = board.get_free_columns(state)
        assert(len(cols) > 0)
        next_states = np.array([board.drop_piece(state, col, player) for col in cols])
        next_states = next_states.reshape(len(next_states), board.NUM_ROWS, board.NUM_COLS, 1)
        values = self.model.predict(next_states).reshape(len(next_states))
        values = player * np.round(values, 5)
        max_value = np.max(values)
        best_cols = [cols[i] for i, value in enumerate(values) if value == max_value]
        return np.random.choice(best_cols)

    def evaluate(self, state, use_target_model=True):
        state = state.reshape(1, board.NUM_ROWS, board.NUM_COLS, 1)
        return self.target_model.predict(state)[0][0] if use_target_model \
            else self.model.predict(state)[0][0]

    def train(self, state, target, stats=None):
        if self.total_steps % self.update_interval == 0:
            self.update_target_model()

        history = self.model.fit(
            x=state.reshape(1, board.NUM_ROWS, board.NUM_COLS, 1),
            y=np.array([[target]]),
            epochs=self.num_epochs, 
            verbose=0)

        stats['loss']['steps'].append(self.total_steps)
        stats['loss']['values'].append(np.sqrt(history.history['loss'][-1]))
        
        self.total_steps += 1

    def load(self, path):
        self.model.load_weights(path)
        self.update_target_model()

    def save(self, path):
        self.model.save_weights(path)

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
        model.add(Dense(1, activation='linear'))

        self.compile_model(model)

        return model
    
    def update_target_model(self):
        self.target_model = clone_model(self.model)
        self.compile_model(self.target_model)
        self.target_model.set_weights(self.model.get_weights())
    
    def compile_model(self, model):
        model.compile(optimizer=Adam(lr=self.learning_rate), loss='mean_squared_error')

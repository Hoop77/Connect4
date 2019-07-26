# -*- coding: utf-8 -*-
import numpy as np
np.random.seed(0)
from keras.models import Sequential, clone_model
from keras.layers import Dense, Conv2D, LeakyReLU, Flatten
from keras.optimizers import Adam
import board
import math

class Agent:
    def __init__(self, 
                 weights=None,
                 gamma=0.95,
                 num_epochs=5,
                 learning_rate=0.001,
                 **kwargs):
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.model = self.build_model()
        self.total_steps = 0
        self.num_epochs = num_epochs

    def act(self, state, player):
        free_cols = board.get_free_columns(state)
        assert(len(free_cols) > 0)
        next_states = np.array([board.drop_piece(state, col, player) for col in free_cols])
        next_states = np.expand_dims(next_states, axis=3)
        values = self.model.predict(next_states).reshape(len(next_states))
        best_col = free_cols[np.argmax(values)]
        return best_col, free_cols, values

    def evaluate(self, state, use_target_model=True):
        state = state.reshape(1, board.NUM_ROWS, board.NUM_COLS, 1)
        return self.model.predict(state)[0][0]

    def train(self, state, target, stats=None):
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

    def save(self, path):
        self.model.save_weights(path)

    def build_model(self):
        input_shape = (board.NUM_ROWS, board.NUM_COLS, 1)
        model = Sequential()
        model.add(Conv2D(32, (4, 4), padding='same', input_shape=input_shape))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(32, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(32, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(32, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(32, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Flatten())
        model.add(Dense(50))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Dense(1, activation='linear'))

        self.compile_model(model)

        return model
    
    def compile_model(self, model):
        model.compile(optimizer=Adam(lr=self.learning_rate), loss='mean_squared_error')

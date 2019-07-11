# -*- coding: utf-8 -*-
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Conv2D, LeakyReLU, Flatten
from keras.optimizers import Adam
from environment import STATE_SHAPE, NUM_ACTIONS, NUM_BOARD_COLS, NUM_BOARD_ROWS

class DQNAgent:
    def __init__(self, weights=None):
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self.build_model()
    
    def predict(self, state):
        state = state.reshape(1, NUM_BOARD_ROWS, NUM_BOARD_COLS, 1)
        return self.model.predict(state)[0]

    def act(self, state):
        act_values = self.predict(state)
        act_values = np.round(act_values)
        return np.argwhere(act_values == np.max(act_values)) 
    
    def act_epsilon_greedy(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(NUM_ACTIONS)
        return self.act(state)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                q_next = self.predict(next_state)
                target = (reward + self.gamma * np.max(q_next))
            target_f = self.predict(state)
            target_f[action] = target
            state = np.expand_dims(state, axis=0)
            target_f = np.expand_dims(target_f, axis=0)
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def build_model(self):
        model = Sequential()
        model.add(Conv2D(20, (5, 5), padding='same', input_shape=(NUM_BOARD_ROWS, NUM_BOARD_COLS, 1)))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(20, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(20, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(30, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(30, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(30, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Conv2D(30, (4, 4), padding='same'))
        model.add(LeakyReLU(alpha=0.3))

        model.add(Flatten(input_shape=(7, 7, 1)))
        model.add(Dense(49))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Dense(7))
        model.add(LeakyReLU(alpha=0.3))
        model.add(Dense(7))
        model.add(LeakyReLU(alpha=0.3))

        model.add(Dense(1, activation='linear'))
        model.compile(optimizer=Adam, loss='mean_squared_error', metrics=['accuracy'])

        # model.summary()
        return model
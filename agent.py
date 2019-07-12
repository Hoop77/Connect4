# -*- coding: utf-8 -*-
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Conv2D, LeakyReLU, Flatten
from environment import STATE_SHAPE, NUM_ACTIONS, NUM_BOARD_COLS, NUM_BOARD_ROWS

class DQNAgent:
    def __init__(self, weights=None):
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.alpha = 0.5
        self.model = self.build_model()
    
    def predict(self, state):
        state = state.reshape(1, NUM_BOARD_ROWS, NUM_BOARD_COLS, 1)
        return self.model.predict(state)[0]

    def act(self, state):
        Q_state = self.predict(state)
        Q_state = np.round(Q_state)
        actions = np.argwhere(Q_state == np.max(Q_state)) 
        if len(actions) == 1:
            return actions[0][0]
        return actions[random.randrange(len(actions))][0]
    
    def act_epsilon_greedy(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(NUM_ACTIONS)
        return self.act(state)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, env, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            Q_target_action = reward
            Q_state = self.predict(state)
            if not done:
                Q_state_action = Q_state[action]
                avail_actions = env.get_action_space()
                Q_next_state = self.predict(next_state)
                Q_max_next_state = np.max([v for a, v in enumerate(Q_next_state) if a in avail_actions])
                Q_target_action = Q_state_action + self.alpha * (reward + self.gamma * Q_max_next_state - Q_state_action)
            Q_target = Q_state
            Q_target[action] = Q_target_action
            state = state.reshape(1, NUM_BOARD_ROWS, NUM_BOARD_COLS, 1)
            Q_target = np.expand_dims(Q_target, axis=0)
            self.model.fit(state, Q_target, epochs=1, verbose=1)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, path):
        self.model.load_weights(path)

    def save(self, path):
        self.model.save_weights(path)

    def build_model(self):
        input_shape = (NUM_BOARD_ROWS, NUM_BOARD_COLS, 1)
        model = Sequential()
        model.add(Conv2D(20, (5, 5), padding='same', input_shape=input_shape))
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

        model.add(Flatten())
        # TODO: try adding another dense layer
        model.add(Dense(NUM_BOARD_COLS, activation='linear'))

        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

        # model.summary()
        return model
import numpy as np
np.random.seed(0)
from keras.models import Sequential, clone_model
from keras.layers import Dense, Conv2D, LeakyReLU, Flatten
from keras.optimizers import Adam, SGD
import board
import math

REWARD_TABLE = {
	board.OUTCOME_NONE: 0.0,
	board.OUTCOME_WIN: 1.0,
	board.OUTCOME_DEFEAT: -1.0,
	board.OUTCOME_DRAW: 0.5
}

class Agent:
    def __init__(self,
                 gamma=0.95,
                 epsilon=0.2,
                 epsilon_min=0.1,
                 learning_rate=0.01,
                 learning_rate_min=0.001,
                 **kwargs):
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.learning_rate = learning_rate
        self.learning_rate_min = learning_rate_min
        self.model = self.build_model()
        self.total_steps = 0

    # used by frontend to predict next move
    def act(self, state, player):
        free_cols = board.get_free_columns(state)
        assert(len(free_cols) > 0)
        next_states = np.array([board.drop_piece(state, col, player) for col in free_cols])
        next_states = np.expand_dims(next_states, axis=3)
        values = self.model.predict(next_states).reshape(len(next_states))
        best_col = free_cols[np.argmax(player * values)]
        return best_col, free_cols, values

    # optimize neural network
    def train(self, state, target):
        history = self.model.fit(
            x=state.reshape(1, board.NUM_ROWS, board.NUM_COLS, 1),
            y=np.array([[target]]),
            verbose=0)

        self.total_steps += 1
        return np.sqrt(history.history['loss'][-1])

    # self-play algorithm simulates one game and learns by outcome
    def self_play(self):
        episode_length = 0
        loss = 0
        state = np.zeros(board.STATE_SHAPE)
        player = board.PLAYER_1
        outcome = board.OUTCOME_NONE
        while outcome == board.OUTCOME_NONE:
            random_move = np.random.rand() <= self.epsilon
            if random_move:
                next_state = board.make_random_move(state, player)
                outcome = board.get_outcome_after_move(next_state, player)
                if outcome == board.OUTCOME_WIN or outcome == board.OUTCOME_DEFEAT:
                    target = REWARD_TABLE[outcome]
                    loss = self.train(state, target)
            else:
                next_state, target = self.make_best_move(state, player, self.gamma)
                loss = self.train(state, target)

            outcome = board.get_outcome_after_move(next_state, player)
            state = next_state
            player = -player
            episode_length += 1

        return loss, self.epsilon, self.learning_rate

    def make_best_move(self, state, player, gamma):
        cols = board.get_free_columns(state)
        next_states = [board.drop_piece(state, col, player) for col in cols]
        outcomes = [board.get_outcome_after_move(next_state, player) for next_state in next_states]
        rewards = np.array([REWARD_TABLE[outcome] for outcome in outcomes])
        not_done = np.array([outcome == board.OUTCOME_NONE for outcome in outcomes]).astype(np.float32)
        values = np.squeeze(self.model.predict(np.expand_dims(next_states, axis=3)))
        targets = rewards + not_done * gamma * values
        targets = player * targets
        target_max_idx = np.argmax(targets)
        target_max = targets[target_max_idx]
        best_next_state = next_states[target_max_idx]
        return best_next_state, player * target_max

    # create neural network
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

    def load(self, path):
        self.model.load_weights(path)

    def save(self, path):
        self.model.save_weights(path)
    
    def compile_model(self, model):
        model.compile(optimizer=SGD(lr=self.learning_rate), loss='mean_squared_error')

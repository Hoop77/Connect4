from agent import DQNAgent
from environment import Environment, RED
from policy import minimax
import math

def train(self, batch_size=32, num_episodes=10000):
    agent = DQNAgent()
    for e in range(num_episodes):
        opponent_policy = lambda state: return minimax(state, 3, -math.inf, math.inf, True, RED)
        env = Environment(opponent_policy=opponent_policy, agent_color=RED, agent_first_turn=True)
        done = False
        while done:
            state = env.get_state()
            action = agent.act_epsilon_greedy(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
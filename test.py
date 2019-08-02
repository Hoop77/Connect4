import numpy as np
import time
import json
from matplotlib import pyplot as plt
import math

def sigmoid(x, a, b, c, d):
    """ General sigmoid function
    a adjusts amplitude
    b adjusts y offset
    c adjusts x offset
    d adjusts slope """
    y = ((a-b) / (1 + np.exp(x-(c/2))**d)) + b
    return y

if __name__ == '__main__':
    num_episodes = 100000
    x = np.arange(48)
    y = sigmoid(x, 0.9, 0.1, num_episodes, 0.3)

    plt.plot(x, y)
    plt.show()

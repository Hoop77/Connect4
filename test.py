import numpy as np
import time
import json
from matplotlib import pyplot as plt
import math

def sigmoid(x, a, b, c, d):

    return y

if __name__ == '__main__':
    num_episodes = 100000
    alpha = 0.01
    test = []
    test2 = []
    for x in range(num_episodes):
        alpha *= 1/(1 + 0.01 * 1000)
        test.append(alpha)
        test2.append(x)

    plt.plot(test, test2)
    plt.show()

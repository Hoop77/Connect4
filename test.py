import numpy as np
import time
import json
from matplotlib import pyplot as plt
import math

def sigmoid(x, a, b, c, d):

    return y

if __name__ == '__main__':
    num_episodes = 1000000
    alpha = 0.01
    epsilon = 0.9
    test = []
    test2 = []
    for x in range(num_episodes):
        alpha = alpha - alpha/num_episodes * 3
        test.append(alpha)
        test2.append(x)

    plt.plot(test2, test)
    plt.show()

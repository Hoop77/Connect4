import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    learning_rates = []
    num_epochs = 1000
    lr = 0.1
    min_lr = 0.01
    decay = (lr - min_lr) / num_epochs
    for epoch in range(num_epochs):
        lr -= decay
        learning_rates.append(lr)
    plt.plot(learning_rates)
    plt.show()
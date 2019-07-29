import numpy as np
from matplotlib import pyplot as plt

def test_keywords(**kwargs):
    print(kwargs)

def test_more(*args, **kwargs):
    print(args)
    print(kwargs)

if __name__ == '__main__':
    array = np.array([4,2,7,1])
    temp = array.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(array))
    print(temp)
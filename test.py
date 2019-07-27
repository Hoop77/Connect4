import numpy as np
from matplotlib import pyplot as plt

def test_keywords(**kwargs):
    print(kwargs)

def test_more(*args, **kwargs):
    print(args)
    print(kwargs)

if __name__ == '__main__':
    test_keywords(hallo='wert1', param=23)
    test_more(42, hallo='wert1', param=23)
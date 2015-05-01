__author__ = 'beniamin'

from numpy import random


class Random2(object):

    def __init__(self):
        self.data_01 = random.randint(0, 2, 100000000)  # Random int numbers {0, 1} - 100 000 000 elements
        self.data_01_ptr = -1

    def rand01(self):
        self.data_01_ptr = (self.data_01_ptr + 1) % 100000000
        return int(self.data_01[self.data_01_ptr])
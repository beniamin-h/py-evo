from collections import deque


class StatsDeque(object):

    def __init__(self):
        self.list = deque(maxlen=978)

    def add(self, value):
        self.list.append(value)

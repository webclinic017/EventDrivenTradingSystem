from collections import deque

class Backtest():
    def __init__(self):
        self.eventQueue = deque()

    def run(self):
        while len(self.eventQueue) > 0:
            event = self.eventQueue.pop()
            
from abc import ABC, abstractmethod
from event import SignalEvent

class Strategy():
    @abstractmethod
    def calculateSignals(self):
        raise NotImplementedError("Should implement calculate_signals()")
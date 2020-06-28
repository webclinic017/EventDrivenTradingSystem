from event import FillEvent, OrderEvent
import pandas as pd
from performance import CAGR, annualVolatility, sharpeRatio, maxDrawdown

class Portfolio():
    def __init__(self, eventQueue, dataHandler, startDate, initialCapital=10000.0):
        """Constructor for a Portfolio object.

        :param eventQueue: Reference to event queue object for updating the event queue when running the algorithm
        :type eventQueue: collections.deque
        :param dataHandler: DataHandler object to retrieve market data for updating the position values
        :type dataHandler: data.DataHandler
        :param startDate: Start date of the portfolio as YYYY-MM-DD
        :type startDate: str
        :param initialCapital: Initial capital allocated to the portfolio in USD, defaults to 10000.0
        :type initialCapital: float, optional
        """
        self.eventQueue = eventQueue
        self.dataHandler = dataHandler
        self.startDate = startDate
        self.universe = self.dataHandler.universe
        self.initialCapital = initialCapital

        initialPositions = dict((k, v) for k, v in [(s, [{'position': 0, 'value': 0}]) for s in self.universe])
        initialPositions['cash'] = self.initialCapital
        initialPositions['total'] = self.initialCapital

        self.positions = pd.DataFrame(
            index=pd.DatetimeIndex(name="datetime", data=[startDate]),
            data=initialPositions
        )

    def updateTimeindex(self, event):
        latestDatetime = self.dataHandler.getLatestBarDatetime(self.universe[0])
        dp = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        dp['datetime'] = latestDatetime


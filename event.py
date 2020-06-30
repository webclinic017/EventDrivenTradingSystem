
class Event():
    """Event base class
    """
    pass

class MarketEvent(Event):
    def __init__(self):
        """Event involving new market data becoming available.
        """
        self.type = "MARKET"

class SignalEvent(Event):
    def __init__(self, strategyId, symbol, datetime, signalType):
        """Event for a signal generated from a strategy.

        :param strategyId: The ID of the strategy which generated the signal
        :type strategyId: int
        :param symbol: The symbol of the asset
        :type symbol: str
        :param datetime: The timestamp at which the signal was generated
        :type datetime: str
        :param signalType: LONG or SHORT
        :type signalType: str
        """
        self.type = "SIGNAL"
        self.strategyId = strategyId
        self.symbol = symbol
        self.datetime = datetime
        self.signalType = signalType

class OrderEvent(Event):
    def __init__(self, symbol, orderType, quantity, direction):
        """Event for an order to be made by the order execution system.

        :param symbol: Name of the symbol to order
        :type symbol: str
        :param orderType: Type of order, either MKT or LMT
        :type orderType: str
        :param quantity: Number of units of an asset
        :type quantity: int
        :param direction: Order direction, either BUY or SELL
        :type direction: str
        """
        self.type = "ORDER"
        self.symbol = symbol
        self.orderType = orderType
        self.quantity = quantity
        self.direction = direction

    def printOrder(self):
        print(
            "Order: Symbol={}, Type={}, Quantity={}, Direction={}".format(
                self.symbol,
                self.orderType,
                self.quantity,
                self.direction
            )
        )

class FillEvent(Event):
    def __init__(self, timestamp, symbol, exchange, quantity, direction, fillPrice, commission=None):
        """Event corresponding to the actual order being filled.
        Equivalent to the response received from a brokerage on the actual
        order details which reflects transaction costs, slippage etc.

        :param timestamp: Date and time when the order was filled
        :type timestamp: [type]
        :param symbol: Symbol transacted
        :type symbol: str
        :param exchange: Name of the stock exchange transacted on
        :type exchange: str
        :param quantity: Number of shares filled in the ordder
        :type quantity: int
        :param direction: Direction of filled order, either BUY or SELL
        :type direction: str
        :param fillPrice: Actual price per unit of the assets transacted
        :type fillPrice: float
        :param commission: Commissions incurred in the transaction, defaults to max(10, 0.001 * fillCost)
        :type commission: float, optional
        """
        self.type = "FILL"
        self.timestamp = timestamp
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fillPrice = fillPrice
        self.commission = commission if commission else self.defaultCommission()
    
    def defaultCommission(self):
        return max(10, 0.001 * self.fillPrice * self.quantity)

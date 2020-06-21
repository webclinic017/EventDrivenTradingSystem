
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
    def __init__(self, symbol, signalType):
        """Event for a signal generated from a strategy.

        :param symbol: [description]
        :type symbol: [type]
        :param signalType: [description]
        :type signalType: [type]
        """
        self.type = "SIGNAL"
        self.symbol = symbol
        self.signalType = signalType

class OrderEvent(Event):
    def __init__(self, symbol, orderType, quantity, direction):
        """Event for an order to be made by the order execution system.

        :param symbol: [description]
        :type symbol: [type]
        :param orderType: [description]
        :type orderType: [type]
        :param quantity: [description]
        :type quantity: [type]
        :param direction: [description]
        :type direction: [type]
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
    def __init__(self):
        """Event corresponding to the actual order being filled.
        Equivalent to the response received from a brokerage on the actual
        order details which reflects transaction costs, slippage etc.
        """
        self.type = "FILL"

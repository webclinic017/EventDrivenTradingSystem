import numpy as np

def CAGR(returns, periods=252):
    """Calculates the CAGR based on a time series of returns.

    :param returns: Percentage returns over a time period
    :type returns: pandas.Series
    :param periods: No. of periods in a year e.g. 252 for a daily returns series, defaults to 252
    :type periods: int, optional
    :return: Compounded Annual Growth Rate (CAGR) where 0.01 = 1%
    :rtype: float
    """
    return returns.add(1.0).product()**(periods / len(returns)) - 1.0

def annualVolatility(returns, periods=252):
    """Calculates the annualised volatility based on a time series of returns.

    :param returns: Percentage returns over a time period
    :type returns: pandas.Series
    :param periods: No. of periods in a year e.g. 252 for a daily returns series, defaults to 252
    :type periods: int, optional
    :return: Annualised Volatility where 0.01 = 1%
    :rtype: float
    """
    return returns.std() * (periods ** 0.5)

def sharpeRatio(returns, periods=252, rfr=0.0):
    """Calculates the Sharpe ratio based on a time series of returns.

    :param returns: Percentage returns over a time period
    :type returns: pandas.Series
    :param periods: No. of periods in a year e.g. 252 for a daily returns series, defaults to 252
    :type periods: int, optional
    :param rfr: Risk free rate, defaults to 0.0
    :type rfr: float, optional
    :return: Sharpe ratio
    :rtype: float
    """
    return (CAGR(returns, periods) - rfr) / annualVolatility(returns, periods)

def maxDrawdown(returns):
    """Calculates the maximum drawdown based on a time series of returns.

    :param returns: Percentage returns over a time period
    :type returns: pandas.Series
    :return: Maximum drawdown amount
    :rtype: float
    """
    value = returns.add(1.0).cumprod()
    return 1.0 - (value / value.cummax()).min()
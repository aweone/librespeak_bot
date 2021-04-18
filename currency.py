from pycbrf.toolbox import ExchangeRates
from time import strftime


def exchange_rate(code):
    return ExchangeRates(strftime("%Y-%m-%d"))[code]

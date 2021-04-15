from pycbrf.toolbox import ExchangeRates
from time import strftime


def exchangeRate(code):
    return ExchangeRates(strftime("%Y-%m-%d"))[code]

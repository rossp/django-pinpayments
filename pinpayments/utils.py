"""
Utility functions without objects
"""
from decimal import Decimal


CURRENCIES = (
    "AUD",
    "USD",
    "NZD",
    "SGD",
    "EUR",
    "GBP",
    "CAD",
    "HKD",
    "JPY",
)


DECIMAL_CURRENCIES = (
    "AUD",
    "USD",
    "NZD",
    "SGD",
    "EUR",
    "GBP",
    "CAD",
    "HKD",
)


SINGLE_UNIT_CURRENCIES = (
    "JPY"
)


def get_value(amount, currency):
    """
    Returns the value of the transfer in the representation of the
    currency it is in, without symbols
    That is, 1000 cents as 10.00, 1000 yen as 1000
    """
    if currency in DECIMAL_CURRENCIES:
        return Decimal(amount)/Decimal(100)
    return Decimal(amount)

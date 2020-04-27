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
    "MYR",
    "THB",
    "PHP",
    "ZAR",
    "IDR",
    "TWD",
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
    "MYR",
    "THB",
    "PHP",
    "ZAR",
    "IDR",
    "TWD",
)

CURRENCY_DETAIL = {
    "AUD": {
        "symbol": "$",
        "name": "Australian dollar",
        },
    "USD": {
        "symbol": "$",
        "name": "US dollar",
        },
    "NZD": {
        "symbol": "$",
        "name": "New Zealand dollar",
        },
    "SGD": {
        "symbol": "$",
        "name": "Singaporean dollar",
        },
    "EUR": {
        "symbol": "€",
        "name": "Euro",
        },
    "GBP": {
        "symbol": "£",
        "name": "Pound sterling",
        },
    "CAD": {
        "symbol": "$",
        "name": "Canadian dollar",
        },
    "HKD": {
        "symbol": "$",
        "name": "Hong Kong dollar",
        },
    "JPY": {
        "symbol": "¥",
        "name": "Japanese yen",
        },
    "MYR": {
        "symbol": "RM",
        "name": "Malaysian ringgit",
        },
    "THB": {
        "symbol": "฿",
        "name": "Thai baht",
        },
    "PHP": {
        "symbol": "₱",
        "name": "Philippine peso",
        },
    "ZAR": {
        "symbol": "R",
        "name": "South African rand",
        },
    "IDR": {
        "symbol": "Rp",
        "name": "Indonesian rupiah",
        },
    "TWD": {
        "symbol": "NT$",
        "name": "New Taiwan dollar",
        },
}


def get_value(amount, currency):
    """
    Returns the value of the transfer in the representation of the
    currency it is in, without symbols
    That is, 1000 cents as 10.00, 1000 yen as 1000
    """
    if currency in DECIMAL_CURRENCIES:
        return Decimal(amount)/Decimal(100)
    return Decimal(amount)

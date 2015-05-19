"""
Utility functions without objects
"""
from decimal import Decimal
from django import VERSION
from django.conf import settings
from pinpayments.exceptions import ConfigError

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
        return Decimal(amount) / Decimal(100)
    return Decimal(amount)


def get_user_model():
    """
        Loads the User model class across different Django versions
    """
    VERSION_MINOR = VERSION[1]
    if VERSION_MINOR >= 5:  # Django 1.5 and up recommends loading the User model class this way.
        from django.contrib.auth import get_user_model as django_get_user_model
        User = django_get_user_model()
        return User

    from django.contrib.auth.models import User
    return User

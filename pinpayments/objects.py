"""
Non-model related objects
"""
from __future__ import unicode_literals

from decimal import Decimal

from django.conf import settings
import requests

from .exceptions import ConfigError, PinError


class PinEnvironment(object):
    """ Container for pin settings """
    def __init__(self, name="test", *args, **kwargs):
        """ Populate contents from Settings """
        if name in ('test', ''):
            name = getattr(settings, 'PIN_DEFAULT_ENVIRONMENT', 'test')

        env_dict = {}
        try:
            env_dict = settings.PIN_ENVIRONMENTS[name]
        except KeyError:
            raise ConfigError("Invalid environment {0}".format(name))

        if not set(env_dict.keys()).issuperset(['key', 'secret', 'host']):
            raise ConfigError(
                "The environment {0} was not correctly defined.\n"
                "Please provide the three fields:\n"
                "\t'key', 'secret', and 'host'".format(name)
            )

        self.name = name
        self.host = env_dict['host']
        self.key = env_dict['key']
        self.secret = env_dict['secret']
        super(PinEnvironment, self).__init__(*args, **kwargs)

    @property
    def auth(self):
        """ Returns auth as expected by requests for Pin """
        return (self.secret, '')

    def _pin_request(self, method, url_tail, payload=None, always_return=False):
        """
        Internal method to abstract common details of calls to Pin API
        """
        method = method.lower()
        if method not in ['get', 'post', 'put']:
            raise Exception(
                "Method for request '{0}' was invalid".format(method)
            )
        requests_method = getattr(requests, method)
        url = 'https://{0}/1{1}'.format(self.host, url_tail)
        if payload is not None:
            response = requests_method(
                url,
                auth=self.auth,
                params=payload,
                headers={'content_type': 'application/json'}
            )
        else:
            response = requests_method(
                url,
                auth=self.auth,
                headers={'content_type': 'application/json'}
            )
        try:
            response_json = response.json()
        except (AttributeError, ValueError):
            if always_return:
                response_json = None
            else:
                raise PinError(
                    "Error retrieving response for environment {0}"
                    "at url {1}".format(self.name, url)
                )

        if not always_return:
            if 'error' in response_json.keys():
                raise PinError(
                    'Error returned from Pin API: {0}:{1}'.format(
                        response_json['error'],
                        response_json['error_description']
                    )
                )

        return (response, response_json)

    def pin_get(self, url_tail, always_return=False):
        """
        Provide a relative URL to access the API for it via GET
        Include the leading /
        Returns a tuple of the response and the decoded JSON
        Provide always_return=True to handle all errors yourself
        """
        return self._pin_request('GET', url_tail, always_return)

    def pin_put(self, url_tail, payload, always_return=False):
        """
        Provide a relative URL to access the API for it via PUT
        Include the leading /
        Returns a tuple of the response and the decoded JSON
        Provide always_return=True to handle all errors yourself
        """
        return self._pin_request('PUT', url_tail, payload, always_return)

    def pin_post(self, url_tail, payload, always_return=False):
        """
        Provide a relative URL to access the API for it via POST
        Include the leading /
        Returns a tuple of the response and the decoded JSON
        Provide always_return=True to handle all errors yourself
        """
        return self._pin_request('POST', url_tail, payload, always_return)

    def get_balance(self, currency="AUD"):
        """
        Query Pin for the balance of a Pin account in the currency given
        Returns a tuple containing Decimals of available and pending balance
        """
        response, response_json = self.pin_get('/balance')
        response_json = response_json['response']

        if not set(response_json.keys()).issuperset(['available', 'pending']):
            raise PinError(
                "The response from Pin was invalid for environment {0}\n"
                "details: {1}".format(self.name, response.text)
            )

        available = set([
            bal['amount'] if bal['currency'] == currency else None
            for bal in response_json['available']
        ])
        if None in available:
            available.remove(None)
        if len(available) != 1:
            raise PinError(
                "Error retrieving available balance for currency {0} "
                "in environment {1}. Available currencies and values are: \n"
                "\t{2}".format(currency, self.name, response_json['available'])
            )
        available_balance = Decimal(list(available)[0])

        pending = set([
            bal['amount'] if bal['currency'] == currency else None
            for bal in response_json['pending']
        ])
        if None in pending:
            pending.remove(None)
        if len(pending) != 1:
            raise PinError(
                "Error retrieving pending balance for currency {0}"
                "in environment {1}. Available currencies and values are: \n"
                "\t{2}".format(currency, self.name, response_json['pending'])
            )
        pending_balance = Decimal(list(pending)[0])

        return (available_balance, pending_balance)

    def get_available_balance(self, currency="AUD"):
        return self.get_balance(currency)[0]

    def get_pending_balance(self, currency="AUD"):
        return self.get_balance(currency)[1]

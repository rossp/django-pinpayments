"""
Models for interacting with Pin, and storing results
"""
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import get_default_timezone
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

import requests
from decimal import Decimal


class ConfigError(Exception):
    """ Errors related to configuration """
    def __init__(self, value):
        self.value = value
        super(ConfigError, self).__init__()

    def __str__(self):
        return repr(self.value)


class PinError(Exception):
    """ Errors related to Pin """
    def __init__(self, value):
        self.value = value
        super(PinError, self).__init__()

    def __str__(self):
        return repr(self.value)


if getattr(settings, 'PIN_ENVIRONMENTS', {}) == {}:
    raise ConfigError("PIN_ENVIRONMENTS not defined.")


TRANS_TYPE_CHOICES = (
    ('Payment', 'Payment'),
    ('Refund', 'Refund'),
)

CARD_TYPES = (
    ('master', 'Mastercard'),
    ('visa', 'Visa'),
)


@python_2_unicode_compatible
class CustomerToken(models.Model):
    """
    A token returned by the Pin Payments Customer API.
    These can be used on a Transaction in lieu of of a Card token, and
    can be reused.
    They are linked to a User record and are typically used for recurring
    billing.
    Card token - difference is that a card can only be used once, for a transaction
    or to be converted to a Customer token. Customer tokens can be reused.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    environment = models.CharField(
        max_length=25, db_index=True, blank=True,
        help_text=_('The name of the Pin environment to use, eg test or live.')
    )
    token = models.CharField(
        _('Token'), max_length=100,
        help_text=_('Generated by Card API or Customers API')
    )
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    active = models.BooleanField(_('Active'), default=True)
    card_type = models.CharField(
        _('Card Type'), max_length=20, blank=True, null=True,
        choices=CARD_TYPES, help_text=_('Determined automatically by Pin')
    )
    card_number = models.CharField(
        _('Card Number'), max_length=100, blank=True, null=True,
        help_text=_('Cleansed by Pin API')
    )
    card_name = models.CharField(
        _('Name on Card'), max_length=100, blank=True, null=True
    )

    def __str__(self):
        return "{0}".format(self.token)

    def save(self, *args, **kwargs):
        if not self.environment:
            self.environment = getattr(settings, 'PIN_DEFAULT_ENVIRONMENT', 'test')
        super(CustomerToken, self).save(*args, **kwargs)

    def new_card_token(self, card_token):
        """ Create a new card token """
        pin_config = getattr(settings, 'PIN_ENVIRONMENTS', {})

        if self.environment not in pin_config.keys():
            raise ConfigError("Invalid environment '{0}'".format(self.environment))

        pin_env = pin_config[self.environment]

        (pin_secret, pin_host) = (pin_env.get('secret', None), pin_env.get('host', None))

        if not (pin_secret and pin_host):
            raise ConfigError(
                "Environment '{0}' does not have "
                "secret and host configured.".format(self.environment)
            )

        payload = {
            'card_token': card_token,
            }

        raw_response = requests.put(
            "https://{0}/1/customers/{1}".format(pin_host, self.token),
            auth=(pin_secret, ''),
            params=payload,
            headers={'content-type': 'application/json'},
        )

        try:
            response = raw_response.json()
        except AttributeError:
            response = None

        if response is None:
            raise PinError('Error retrieving response')

        else:
            if 'error' in response.keys():
                raise PinError(
                    'Error returned from Pin API: {0}'.format(
                        response['error_description']
                    )
                )
            else:
                self.card_number = response['response']['card']['display_number']
                self.card_type = response['response']['card']['scheme']
                self.card_name = response['response']['card']['name']
                self.save()
                return True

        return False

    @classmethod
    def create_from_card_token(cls, card_token, user, environment=''):
        """ Create a customer token from a card token """
        pin_config = getattr(settings, 'PIN_ENVIRONMENTS', {})

        payload = {
            'email': user.email,
            'card_token': card_token,
            }

        if not environment:
            environment = getattr(settings, 'PIN_DEFAULT_ENVIRONMENT', 'test')

        if environment not in pin_config.keys():
            raise ConfigError("Invalid environment '{0}'".format(environment))

        pin_env = pin_config[environment]

        (pin_secret, pin_host) = (pin_env.get('secret', None), pin_env.get('host', None))

        if not (pin_secret and pin_host):
            raise ConfigError(
                "Environment '{0}' does not"
                "have secret and host configured.".format(environment)
            )

        raw_response = requests.post(
            "https://{0}/1/customers".format(pin_host),
            auth=(pin_secret, ''),
            params=payload,
            headers={'content-type': 'application/json'},
        )

        try:
            response = raw_response.json()
        except AttributeError:
            response = None

        if response is None:
            raise PinError('Error retrieving response')

        else:
            if 'error' in response.keys():
                raise PinError(
                    'Error returned from Pin API: {0}'.format(
                        response['error_description']
                    )
                )
            else:
                customer = CustomerToken()
                customer.user = user
                customer.token = response['response']['token']
                customer.environment = environment
                customer.card_number = response['response']['card']['display_number']
                customer.card_type = response['response']['card']['scheme']
                customer.card_name = response['response']['card']['name']
                customer.save()

                return customer


@python_2_unicode_compatible
class PinTransaction(models.Model):
    """
    PinTransaction - model to hold response data from the pin.net.au
    Charge API. Note we capture the card and/or customer token, but
    there's no FK to your own customers table. That's for you to do
    in your own code.
    """
    date = models.DateTimeField(
        _('Date'), db_index=True, help_text=_(
            'Time this transaction was put in the database. '
            'May differ from the time that PIN reports the transaction.'
        )
    )
    environment = models.CharField(
        max_length=25, db_index=True, blank=True,
        help_text=_('The name of the Pin environment to use, eg test or live.')
    )
    amount = models.DecimalField(
        _('Amount (Dollars)'), max_digits=10, decimal_places=2
    )
    fees = models.DecimalField(
        _('Transaction Fees'), max_digits=10, decimal_places=2,
        default=Decimal("0.00"), blank=True, null=True, help_text=_(
            'Fees charged to you by Pin, for this transaction, in dollars'
        )
    )
    description = models.TextField(
        _('Description'), blank=True, null=True,
        help_text=_('As provided when you initiated the transaction')
    )
    processed = models.BooleanField(
        _('Processed?'), default=False,
        help_text=_('Has this been sent to Pin yet?')
    )
    succeeded = models.BooleanField(
        _('Success?'), default=False,
        help_text=_('Was the transaction approved?')
    )
    currency = models.CharField(
        _('Currency'), max_length=100, default='AUD',
        help_text=_('Currency transaction was processed in')
    )
    transaction_token = models.CharField(
        _('Pin API Transaction Token'), max_length=100, blank=True, null=True,
        db_index=True, help_text=_('Unique ID from Pin for this transaction')
    )
    card_token = models.CharField(
        _('Pin API Card Token'), max_length=40, blank=True, null=True,
        help_text=_(
            'Card token used for this transaction (Card API and Web Forms)'
        )
    )
    customer_token = models.ForeignKey(
        CustomerToken, blank=True, null=True,
        help_text=_('Provided by Customer API')
    )
    pin_response = models.CharField(
        _('API Response'), max_length=255, blank=True, null=True,
        help_text=_('Response text, usually Success!')
    )
    ip_address = models.GenericIPAddressField(
        help_text=_('IP Address used for payment')
    )
    email_address = models.EmailField(
        _('E-Mail Address'), max_length=100, help_text=_('As passed to Pin.')
    )
    card_address1 = models.CharField(
        _('Cardholder Street Address'), max_length=100, blank=True, null=True,
        help_text=_('Address entered by customer to process this transaction')
    )
    card_address2 = models.CharField(
        _('Cardholder Street Address Line 2'), max_length=100, blank=True,
        null=True
    )
    card_city = models.CharField(
        _('Cardholder City'), max_length=100, blank=True, null=True
    )
    card_state = models.CharField(
        _('Cardholder State'), max_length=100, blank=True, null=True
    )
    card_postcode = models.CharField(
        _('Cardholder Postal / ZIP Code'), max_length=100, blank=True,
        null=True
    )
    card_country = models.CharField(
        _('Cardholder Country'), max_length=100, blank=True, null=True
    )
    card_number = models.CharField(
        _('Card Number'), max_length=100, blank=True, null=True,
        help_text=_('Cleansed by Pin API')
    )
    card_type = models.CharField(
        _('Card Type'), max_length=20, blank=True, null=True,
        choices=CARD_TYPES, help_text=_('Determined automatically by Pin')
    )
    pin_response_text = models.TextField(
        _('Complete API Response'), blank=True, null=True,
        help_text=_('The full JSON response from the Pin API')
    )

    def save(self, *args, **kwargs):
        if not (self.card_token or self.customer_token):
            raise PinError("Must provide card_token or customer_token")

        if self.card_token and self.customer_token:
            raise PinError("Can only provide card_token OR customer_token, not both")

        if not self.environment:
            self.environment = getattr(settings, 'PIN_DEFAULT_ENVIRONMENT', 'test')

        if self.environment not in getattr(settings, 'PIN_ENVIRONMENTS', {}):
            raise PinError("Pin Environment '{0}' does not exist".format(self.environment))

        if not self.date:
            now = datetime.now()
            if settings.USE_TZ:
                now = timezone.make_aware(now, get_default_timezone())
            self.date = now

        super(PinTransaction, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.id)

    class Meta:
        verbose_name = 'PIN.net.au Transaction'
        verbose_name_plural = 'PIN.net.au Transactions'
        ordering = ['-date']

    def process_transaction(self):
        """ Send the data to Pin for processing """
        if self.processed:
            """
            can only attempt to process once.
            """
            return None

        self.processed = True
        self.save()

        payload = {
            'email': self.email_address,
            'description': self.description,
            'amount': int(self.amount * 100),
            'currency': self.currency,
            'ip_address': self.ip_address,
        }
        if self.card_token:
            payload['card_token'] = self.card_token
        else:
            payload['customer_token'] = self.customer_token.token

        pin_env = getattr(settings, 'PIN_ENVIRONMENTS', {})[self.environment]

        (pin_secret, pin_host) = (pin_env.get('secret', None), pin_env.get('host', None))

        if not (pin_secret and pin_host):
            raise ConfigError(
                "Environment '{0}' does not have "
                "secret and host configured.".format(self.environment)
            )

        raw_response = requests.post(
            "https://{0}/1/charges".format(pin_host),
            auth=(pin_secret, ''),
            params=payload,
            headers={'content-type': 'application/json'},
        )

        try:
            response = raw_response.json()
        except AttributeError:
            response = None

        self.pin_response_text = raw_response.text,

        if response is None:
            self.pin_response = 'Failure.'
        elif 'error' in response.keys():
            if 'messages' in response.keys():
                if 'message' in response['messages'][0].keys():
                    self.pin_response = 'Failure: {0}'.format(
                        response['messages'][0]['message']
                    )
            else:
                self.pin_response = 'Failure: {0}'.format(
                    response['error_description']
                )
            self.transaction_token = response.get('charge_token', None)
        else:
            self.succeeded = True
            self.transaction_token = response['response']['token']
            self.fees = response['response']['total_fees'] / Decimal("100.00")
            self.pin_response = response['response']['status_message']
            self.card_address1 = response['response']['card']['address_line1']
            self.card_address2 = response['response']['card']['address_line2']
            self.card_city = response['response']['card']['address_city']
            self.card_state = response['response']['card']['address_state']
            self.card_postcode = response['response']['card']['address_postcode']
            self.card_country = response['response']['card']['address_country']
            self.card_number = response['response']['card']['display_number']
            self.card_type = response['response']['card']['scheme']
        self.save()

        return self.pin_response


@python_2_unicode_compatible
class BankAccount(models.Model):
    """ A representation of a bank account, as stored by Pin. """
    token = models.CharField(
        _('Pin API Bank account token'), max_length=40,
        help_text="A bank account token provided by Pin"
    )
    bank_name = models.CharField(
        _('Bank Name'), max_length=100,
        help_text="The name of the bank at which this account is held"
    )
    branch = models.CharField(
        _('Branch name'), max_length=100, blank=True,
        help_text="The name of the branch at which this account is held"
    )
    name = models.CharField(
        _('Recipient Name'), max_length=100,
        help_text="The name of the bank account"
    )
    bsb = models.IntegerField(
        _('BSB'), max_length=6,
        help_text="The BSB (Bank State Branch) code of the bank account."
    )
    number = models.CharField(
        _('BSB'), max_length=20,
        help_text="The account number of the bank account"
    )
    environment = models.CharField(
        max_length=25, db_index=True, blank=True,
        help_text=_('The name of the Pin environment to use, eg test or live.')
    )

    def __str__(self):
        return "{0}".format(self.token)


@python_2_unicode_compatible
class PinRecipient(models.Model):
    """
    A token-based method for transferring funds via Pin
    """
    token = models.CharField(
        _('Pin API recipient token'), max_length=40,
        help_text="A recipient token provided by Pin"
    )
    email = models.EmailField(
        _('Email Address'), max_length=100, help_text=_('As passed to Pin.')
    )
    name = models.CharField(
        _('Recipient Name'), max_length=100, blank=True, null=True,
        help_text="Optional. The name by which the recipient is referenced"
    )
    created = models.DateTimeField(_("Time created"), auto_now_add=True)
    bank_account = models.ForeignKey(
        BankAccount, verbose_name=_("The bank account of this recipient"),
        blank=True, null=True
    )
    environment = models.CharField(
        max_length=25, db_index=True, blank=True,
        help_text=_('The name of the Pin environment to use, eg test or live.')
    )

    def __str__(self):
        return "{0}".format(self.token)

    @classmethod
    def create_with_bank_account(cls, email, account_name, bsb, number, name="", env='test'):
        """ Creates a new recipient from a provided token """
        pin_env = getattr(settings, 'PIN_ENVIRONMENTS', {})[env]
        (pin_secret, pin_host) = (pin_env.get('secret', None), pin_env.get('host', None))
        if not (pin_secret and pin_host):
            raise ConfigError(
                "Environment '{0}' does not have "
                "secret and host configured.".format(env)
            )

        payload = {
            'email': email,
            'name': name,
            'bank_account[name]': account_name,
            'bank_account[bsb]': bsb,
            'bank_account[number]': number
        }

        raw_response = requests.post(
            "https://{0}/1/recipients".format(pin_host),
            auth=(pin_secret, ''),
            params=payload,
            headers={'content-type': 'application/json'},
        )

        try:
            response = raw_response.json()
        except AttributeError:
            response = None

        if response is None:
            raise PinError('Error retrieving response')

        if 'error_description' in response.keys():
            raise PinError(
                'Error returned from Pin API: {0}'.format(
                    response['error_description']
                )
            )

        bank_account = BankAccount()
        bank_account.bank_name = response['response']['bank_account']['bank_name']
        bank_account.branch = response['response']['bank_account']['branch']
        bank_account.bsb = response['response']['bank_account']['bsb']
        bank_account.name = response['response']['bank_account']['name']
        bank_account.number = response['response']['bank_account']['number']
        bank_account.token = response['response']['bank_account']['token']
        bank_account.environment = env
        bank_account.save()

        new_recipient = PinRecipient()
        new_recipient.token = response['response']['token']
        new_recipient.email = response['response']['email']
        new_recipient.name = response['response']['name']
        new_recipient.bank_account = bank_account
        new_recipient.environment = env
        new_recipient.save()

        return new_recipient

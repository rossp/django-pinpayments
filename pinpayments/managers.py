from __future__ import absolute_import, unicode_literals

from django.db import models
from pinpayments.objects import PinEnvironment
from django.db.models.loading import get_model
from pinpayments.exceptions import PinError


class CardTokenManager(models.Manager):
    """
        Manager class for CardToken, separates API calls and model logic away from the
        Model's class impl for sanity and separation of concern reasons.
    """

    def create_from_data(self, data):
        """
            Creates a new CardToken instance from a PIN response
        """
        card = self.model()
        card.token = data.get('token')
        card.scheme = data.get('scheme')
        card.name = data.get('name')
        card.display_number = data.get('display_number')
        card.expiry_month = data.get('expiry_month')
        card.expiry_year = data.get('expiry_year')
        card.address_line1 = data.get('address_line1')
        card.address_line2 = data.get('address_line2')
        card.address_city = data.get('address_city')
        card.address_state = data.get('address_state')
        card.address_postcode = data.get('address_postcode')
        card.address_country = data.get('address_country')
        card.primary = data.get('primary')
        card.save()
        return card


class CustomerTokenManager(models.Manager):
    """
        Manager class for CustomerToken, separates API calls and model logic away from the
        Model's class impl for sanity and separation of concern reasons.

        Variables and parameter semantics: because the actual model names in this app are a
        little confusing with the API paramters:
            CustomerToken instances -> customer
            CardToken instances -> `card`
            API customer token -> `customer_token`
            API card token -> `card_token`
    """

    def set_primary_card_models(self, customer, primary_card, data={}):
        """
        Handles keeping the primary CardTokens of cards on CustomerTokens in sync.

        TODO: update the card_token attributes from the returned data if needed.
        """
        customer.cards.exclude(pk=primary_card.pk).filter(primary=True).update(primary=False)
        primary_card.primary = True
        primary_card.save()

    def update_primary_card_for_customer(self, customer, card):
        """
            Sets the primary CardToken for a given CustomerToken.
        """
        payload = {}

        payload.update({
            'primary_card_token': card.token
        })

        pin_env = PinEnvironment(customer.environment)
        url_tail = "/customers/{0}".format(customer.token)
        data = pin_env.pin_put(url_tail, payload)[1]['response']

        self.set_primary_card_models(customer, card, data)

    def add_card_token_to_customer(self, customer, card_token):
        """
            Creates a new CardToken instance from a card_token and attaches it to a customer's cards.
        """
        CardToken = get_model('pinpayments', 'CardToken')
        pin_env = PinEnvironment(customer.environment)
        payload = {'card_token': card_token}

        url_tail = "/customers/{0}/cards".format(customer.token)
        data = pin_env.pin_post(url_tail, payload)[1]['response']

        card = CardToken.objects.create_from_data(data)
        customer.cards.add(card)

        if card.primary:
            self.set_primary_card_models(customer, card)
        return card

    def create_from_card_token(self, card_token, user, environment=None):
        """
            Create a new CustomerToken from a card_token and attacheds a
            CardToken to the CustomerToken instance.
        """
        CardToken = get_model('pinpayments', 'CardToken')
        CustomerToken = self.model

        pin_env = PinEnvironment(environment)
        payload = {'email': user.email, 'card_token': card_token}
        data = pin_env.pin_post("/customers", payload)[1]['response']
        customer = CustomerToken.objects.create(
            user=user,
            token=data['token'],
            environment=environment,
        )

        # attach the card object
        card = CardToken.objects.create_from_data(data.get('card'))
        customer.cards.add(card)

        if card.primary:
            self.set_primary_card_models(customer, card)

        return customer

    def delete_card_from_customer(self, customer, card):
        """
            Deletes a CardToken from a CustomerToken instance.
        """
        pin_env = PinEnvironment(customer.environment)

        if card not in customer.cards.all():
            raise PinError("The CardToken does not belong to the CustomerToken and cannot be deleted.")

        url_tail = "/customers/{0}/cards/{1}".format(customer.token, card.token)
        data = pin_env.pin_delete(url_tail, {})

        # success
        customer.cards.remove(card)
        card.delete()

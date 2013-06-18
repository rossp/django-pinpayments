from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from pinpayments.models import PinTransaction

class ModelsCase(TestCase):
    # Need to override the setting so we can delete it, not sure why.
    @override_settings(PIN_DEFAULT_ENVIRONMENT=None)
    def test_save_defaults(self):
        # Unset PIN_DEFAULT_ENVIRONMENT to test that the enviroment defaults
        # to 'test'.
        del settings.PIN_DEFAULT_ENVIRONMENT

        t = PinTransaction()
        t.card_token = '12345'
        t.ip_address = '127.0.0.1'
        t.amount = 500
        t.currency = 'AUD'
        t.email_address = 'test@example.com'
        t.save()

        self.assertEqual(t.environment, 'test')
        self.assertTrue(t.date)

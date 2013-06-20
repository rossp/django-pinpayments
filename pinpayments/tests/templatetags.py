from datetime import datetime
from django.conf import settings
from django.template import TemplateSyntaxError
from django.test import TestCase
from django.test.utils import override_settings
from pinpayments.templatetags.pin_payment_tags import pin_form, pin_header

ENV_OK = {
    'staging': {
        'key': 'key1',
        'secret': 'secret1',
        'host': 'test-api.pin.net.au',
    },
}

ENV_MISSING_KEY = {
    'test': {
        'secret': 'secret1',
        'host': 'test-api.pin.net.au',
    },
}

ENV_MISSING_HOST = {
    'test': {
        'key': 'key1',
        'secret': 'secret1',
    },
}

class TemplateTagsTests(TestCase):
    def test_pin_form(self):
        form = pin_form()
        current_year = datetime.now().year
        self.assertEqual(form['pin_cc_years'],
            range(current_year, current_year + 15))

    def test_pin_header_default_environment(self):
        header = pin_header()
        self.assertEqual(header['pin_environment'], 'test')

    @override_settings(PIN_ENVIRONMENTS={})
    def test_pin_header_no_environments(self):
        self.assertRaises(TemplateSyntaxError, pin_header)

    def test_pin_header_default_environment(self):
        with self.assertRaises(TemplateSyntaxError):
            pin_header(environment='should not exist')

    @override_settings(PIN_ENVIRONMENTS=ENV_MISSING_KEY)
    def test_pin_header_no_key(self):
        self.assertRaises(TemplateSyntaxError, pin_header)

    @override_settings(PIN_ENVIRONMENTS=ENV_MISSING_HOST)
    def test_pin_header_no_host(self):
        self.assertRaises(TemplateSyntaxError, pin_header)

    @override_settings(PIN_ENVIRONMENTS=ENV_OK)
    def test_pin_header_success(self):
        header = pin_header(environment='staging')
        self.assertEqual(header['pin_environment'], 'staging')
        self.assertEqual(header['pin_public_key'], 'key1')
        self.assertEqual(header['pin_host'], 'test-api.pin.net.au')

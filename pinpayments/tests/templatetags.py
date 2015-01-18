""" Template Tag test classes """
from datetime import datetime
from django.template import TemplateSyntaxError
from django.template.context import RequestContext
from django.test import TestCase, RequestFactory
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
    """ Test the template tags """
    def __init__(self, *args, **kwargs):
        """ define attributes """
        self.factory = None
        self.request = None
        self.context = None
        super(TemplateTagsTests, self).__init__(*args, **kwargs)

    def set_up(self):
        """ Common setup for all methods """
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.context = RequestContext(self.request)

    def test_pin_form(self):
        """ Check the years which are output """
        form = pin_form(self.context)
        current_year = datetime.now().year
        self.assertEqual(
            form['pin_cc_years'],
            range(current_year, current_year + 15)
        )

    def test_pin_header_default_env(self):
        """ Check 'test' is the default environment """
        header = pin_header(self.context)
        self.assertEqual(header['pin_environment'], 'test')

    @override_settings(PIN_ENVIRONMENTS={})
    def test_pin_header_no_env(self):
        """ Check errors are raised when no environments are present """
        self.assertRaises(TemplateSyntaxError, pin_header, self.context)

    def test_pin_header_bad_env(self):
        """ Check an error is raised when a bad environment is requested """
        with self.assertRaises(TemplateSyntaxError):
            pin_header(self.context, environment='should not exist')

    @override_settings(PIN_ENVIRONMENTS=ENV_MISSING_KEY)
    def test_pin_header_no_key(self):
        self.assertRaises(TemplateSyntaxError, pin_header, self.context)

    @override_settings(PIN_ENVIRONMENTS=ENV_MISSING_HOST)
    def test_pin_header_no_host(self):
        self.assertRaises(TemplateSyntaxError, pin_header, self.context)

    @override_settings(PIN_ENVIRONMENTS=ENV_OK)
    def test_pin_header_success(self):
        """ Check the values of the environment are properly extracted """
        header = pin_header(self.context, environment='staging')
        self.assertEqual(header['pin_environment'], 'staging')
        self.assertEqual(header['pin_public_key'], 'key1')
        self.assertEqual(header['pin_host'], 'test-api.pin.net.au')

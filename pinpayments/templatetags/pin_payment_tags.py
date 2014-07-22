from django import template
from django.conf import settings

register = template.Library()


def pin_header(context, environment=''):
    """
    pin_header - Renders the JavaScript required for Pin.js payments.
    This will also include the Pin.js file from pin.net.au.
    Optionally accepts an 'environment' (eg test/live) as a paramater, 
    otherwise the default will be used.
    """
    if environment == '':
        environment = getattr(settings, 'PIN_DEFAULT_ENVIRONMENT', 'test')

    pin_config = getattr(settings, 'PIN_ENVIRONMENTS', {})

    if pin_config == {}:
        raise template.TemplateSyntaxError("PIN_ENVIRONMENTS setting does not exist.")

    if environment not in pin_config.keys():
        raise template.TemplateSyntaxError("Environment '%s' does not exist in PIN_ENVIRONMENTS" % environment)

    pin_env = pin_config[environment]

    (pin_key, pin_host) = (pin_env.get('key', None), pin_env.get('host', None))

    if not (pin_key and pin_host):
        raise template.TemplateSyntaxError("Environment '%s' does not have key and host configured." % environment)

    return {
            'pin_environment': environment,
            'pin_public_key': pin_key,
            'pin_host': pin_host,
            'request': context,
            }


def pin_form(context):
    """
    pin_form - renders a simple HTML form
    Should be inside existing <form class='pin'>...</form> tags.
    """
    from datetime import datetime
    current_year = datetime.now().year
    return {
            'pin_cc_years': range(current_year, current_year + 15),
            'request': context,
            }

register.inclusion_tag('pinpayments/pin_headers.html', takes_context=True)(pin_header)
register.inclusion_tag('pinpayments/pin_form.html', takes_context=True)(pin_form)

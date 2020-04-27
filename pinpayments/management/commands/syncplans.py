from django.core.management.base import BaseCommand, CommandError
from pinpayments.models import PinPlan
from django.conf import settings

class Command(BaseCommand):
    help = 'Retrieves Plan configuration from Pin Payments. Updates all configured environments unless an optional environment name is provided.'

    def add_arguments(self, parser):
        parser.add_argument('environment', nargs='?', type=str, default='all_environments')

    def handle(self, *args, **options):
        env = options['environment']
        if env == 'all_environments':
            for pin_env in settings.PIN_ENVIRONMENTS.keys():
                if settings.PIN_ENVIRONMENTS[pin_env].get('secret'):
                    sync_env(pin_env)
        else:
            sync_env(env)

def sync_env(env):
    result = PinPlan.get_from_pin(env)
    print("[{}] Created {} plan(s)".format(env, result['new']))
    print("[{}] Updated {} plan(s)".format(env, result['updated']))

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.utils import OperationalError, ProgrammingError


def migrate_customer_card_data_to_cardtokens(apps, schema_editor):
    CustomerToken = apps.get_model("pinpayments", "CustomerToken")
    CardToken = apps.get_model("pinpayments", "CardToken")
    try:
        for customer_token in CustomerToken.objects.all():
            card_token = CardToken()
            card_token.scheme = customer_token.card_type
            card_token.display_number = customer_token.card_number
            card_token.name = customer_token.card_name
            card_token.token = customer_token.token
            card_token.save()
            customer_token.cards.add(card_token)
    except (OperationalError, ProgrammingError):
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('pinpayments', '0002_auto_20150519_0110'),
    ]

    operations = [
        migrations.RunPython(migrate_customer_card_data_to_cardtokens),
    ]

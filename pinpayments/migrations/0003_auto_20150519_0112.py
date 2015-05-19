# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_customer_card_data_to_cardtokens(apps, schema_editor):
    CustomerToken = apps.get_model("pinpayments", "CustomerToken")
    CardToken = apps.get_model("pinpayments", "CardToken")
    for customer_token in CustomerToken.objects.all():
        card_token = CardToken()
        card_token.scheme = customer_token.card_type
        card_token.display_number = customer_token.card_number
        card_token.name = customer_token.card_name
        card_token.expiry_month = customer_token.card_expiry_month
        card_token.expiry_year = customer_token.card_expiry_year
        card_token.save()
        customer_token.cards.add(card_token)


class Migration(migrations.Migration):

    dependencies = [
        ('pinpayments', '0002_auto_20150519_0110'),
    ]

    operations = [
        migrations.RunPython(migrate_customer_card_data_to_cardtokens),
    ]

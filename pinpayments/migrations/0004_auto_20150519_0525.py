# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinpayments', '0003_auto_20150519_0112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customertoken',
            name='card_name',
        ),
        migrations.RemoveField(
            model_name='customertoken',
            name='card_number',
        ),
        migrations.RemoveField(
            model_name='customertoken',
            name='card_type',
        ),
        migrations.AlterField(
            model_name='customertoken',
            name='cards',
            field=models.ManyToManyField(to='pinpayments.CardToken', blank=True),
            preserve_default=True,
        ),
    ]

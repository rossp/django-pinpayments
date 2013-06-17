# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PinTransaction'
        db.create_table(u'pinpayments_pintransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('environment', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=25, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('fees', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('succeeded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='AUD', max_length=100)),
            ('transaction_token', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100, null=True, blank=True)),
            ('card_token', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('pin_response', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('card_address1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('card_address2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('card_city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('card_state', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('card_postcode', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('card_country', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('card_number', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('card_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('pin_response_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pinpayments', ['PinTransaction'])


    def backwards(self, orm):
        # Deleting model 'PinTransaction'
        db.delete_table(u'pinpayments_pintransaction')


    models = {
        u'pinpayments.pintransaction': {
            'Meta': {'ordering': "['-date']", 'object_name': 'PinTransaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'card_address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_postcode': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_token': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'AUD'", 'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'environment': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'blank': 'True'}),
            'fees': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'pin_response': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pin_response_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'succeeded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transaction_token': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['pinpayments']
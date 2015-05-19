# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from . import User, user_orm_label, user_model_label, user_model_definition

from . import User, user_orm_label, user_model_label, user_model_definition


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CardToken'
        db.create_table(u'pinpayments_cardtoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('environment', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=25, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('scheme', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('display_number', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('expiry_month', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('expiry_year', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('address_line1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('address_line2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('address_city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('address_state', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('address_postcode', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('address_country', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('primary', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'pinpayments', ['CardToken'])

        # Adding M2M table for field cards on 'CustomerToken'
        m2m_table_name = db.shorten_name(u'pinpayments_customertoken_cards')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customertoken', models.ForeignKey(orm[u'pinpayments.customertoken'], null=False)),
            ('cardtoken', models.ForeignKey(orm[u'pinpayments.cardtoken'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customertoken_id', 'cardtoken_id'])


    def backwards(self, orm):
        # Deleting model 'CardToken'
        db.delete_table(u'pinpayments_cardtoken')

        # Removing M2M table for field cards on 'CustomerToken'
        db.delete_table(db.shorten_name(u'pinpayments_customertoken_cards'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pinpayments.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'bsb': ('django.db.models.fields.IntegerField', [], {}),
            'environment': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'})
        },
        u'pinpayments.cardtoken': {
            'Meta': {'ordering': "[u'created']", 'object_name': 'CardToken'},
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_postcode': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'environment': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'blank': 'True'}),
            'expiry_month': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'expiry_year': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'primary': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'scheme': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pinpayments.customertoken': {
            'Meta': {'object_name': 'CustomerToken'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'card_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pinpayments.CardToken']", 'symmetrical': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'environment': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % user_orm_label})
        },
        u'pinpayments.pinrecipient': {
            'Meta': {'object_name': 'PinRecipient'},
            'bank_account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinpayments.BankAccount']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'environment': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'})
        },
        u'pinpayments.pintransaction': {
            'Meta': {'ordering': "[u'-date']", 'object_name': 'PinTransaction'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'card_address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_postcode': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'card_token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'card_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "u'AUD'", 'max_length': '100'}),
            'customer_token': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinpayments.CustomerToken']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'environment': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'blank': 'True'}),
            'fees': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'pin_response': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pin_response_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'succeeded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transaction_token': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'pinpayments.pintransfer': {
            'Meta': {'object_name': 'PinTransfer'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pin_response_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinpayments.PinRecipient']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'transfer_token': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        user_model_label: user_model_definition,
    }

    complete_apps = ['pinpayments']
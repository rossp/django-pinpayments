from django.contrib import admin
from pinpayments.models import PinTransaction

class PinAdmin(admin.ModelAdmin):
    list_display = ('date', 'processed', 'succeeded', 'environment', 'amount', 'currency', 'email_address', 'pin_response', 'ip_address', 'transaction_token',)
    search_fields = ('email_address', 'ip_address', 'card_token', 'transaction_token',)
    list_filter = ('processed', 'succeeded', 'environment', 'currency', )
    date_hierarchy = 'date'

admin.site.register(PinTransaction, PinAdmin)

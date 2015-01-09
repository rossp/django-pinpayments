""" Administrative access to Pin data """
from django.contrib import admin
from pinpayments.models import PinRecipient, PinTransaction, CustomerToken


class PinTransactionAdmin(admin.ModelAdmin):
    """ Inspect transactions from here """
    list_display = (
        'date',
        'processed',
        'succeeded',
        'environment',
        'amount',
        'currency',
        'email_address',
        'pin_response',
        'ip_address',
        'transaction_token',
    )
    search_fields = (
        'email_address',
        'ip_address',
        'card_token',
        'transaction_token',
    )
    list_filter = ('processed', 'succeeded', 'environment', 'currency')
    date_hierarchy = 'date'
    readonly_fields = (
        'date',
        'description',
        'processed',
        'succeeded',
        'environment',
        'amount',
        'currency',
        'fees',
        'email_address',
        'pin_response',
        'ip_address',
        'transaction_token',
        'card_token',
        'customer_token',
        'email_address',
        'card_address1',
        'card_address2',
        'card_city',
        'card_state',
        'card_postcode',
        'card_country',
        'card_number',
        'card_type',
        'pin_response_text',
    )


class PinTransactionInline(admin.TabularInline):
    """
    Used to show transactions for a particular customer token, if using
    the Customer API.
    """
    model = PinTransaction
    fields = (
        'date',
        'processed',
        'succeeded',
        'environment',
        'amount',
        'currency',
        'transaction_token',
        'ip_address',
    )
    readonly_fields = fields


class TokenAdmin(admin.ModelAdmin):
    """ Shows customer tokens """
    list_display = (
        'token',
        'user',
        'environment',
        'created',
        'active',
        'card_type',
        'card_number',
    )
    search_fields = ('token', 'card_number')
    list_filter = ('environment', 'card_type', 'active')
    date_hierarchy = 'created'
    inlines = (PinTransactionInline,)
    readonly_fields = ('environment', 'token', 'card_type', 'card_number')


class PinRecipientAdmin(admin.ModelAdmin):
    """ Allows viewing and re-aliasing PinRecipients """
    list_display = (
        'token',
        'email',
        'name',
        'environment',
        'created',
        'bank_account',
    )
    search_fields = ('token', 'email', 'name')
    list_filter = ('environment',)
    date_hierarchy = 'created'
    readonly_fields = list_display  # all the fields


admin.site.register(PinRecipient, PinRecipientAdmin)
admin.site.register(PinTransaction, PinTransactionAdmin)
admin.site.register(CustomerToken, TokenAdmin)

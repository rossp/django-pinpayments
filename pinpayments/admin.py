""" Administrative access to Pin data """
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from pinpayments.models import (
    PinRecipient, PinTransfer, PinTransaction, CustomerToken
, CardToken)


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
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False


class CustomerTokenAdmin(admin.ModelAdmin):
    """ Shows customer tokens """
    list_display = (
        'user',
        'token',
        'environment',
        'created',
        'active',
    )
    search_fields = ('token', )
    list_filter = ('environment', 'active')
    date_hierarchy = 'created'
    readonly_fields = ('environment', 'token')


class PinTransferAdmin(admin.ModelAdmin):
    """ Shows the details of a transfer """
    list_display = (
        'created',
        'get_value',
        'recipient',
        'status',
    )
    search_fields = (
        'recipient',
        'transfer_token',
    )
    date_hierarchy = 'created'
    readonly_fields = (
        'transfer_token',
        'status',
        'currency',
        'description',
        'amount',
        'recipient',
        'created',
        'pin_response_text',
    )

    def has_add_permission(self, request):
        return False

    def get_value(self, obj):
        return "{0:.2f} {1}".format(obj.value, obj.currency)
    get_value.short_description = _('Value')
    get_value.admin_order_field = 'amount'


class PinTransferInline(admin.TabularInline):
    """ Shows transfers under recipients """
    model = PinTransfer
    fields = [
        'created',
        'get_value',
        'status',
        'currency',
        'description',
        'transfer_token',
    ]
    readonly_fields = fields
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False

    def get_value(self, obj):
        return "{0:.2f} {1}".format(obj.value, obj.currency)
    get_value.short_description = _('Value')


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
    inlines = (PinTransferInline,)
    readonly_fields = list_display  # all the fields


admin.site.register(PinRecipient, PinRecipientAdmin)
admin.site.register(PinTransaction, PinTransactionAdmin)
admin.site.register(CustomerToken, CustomerTokenAdmin)
admin.site.register(CardToken)
admin.site.register(PinTransfer, PinTransferAdmin)

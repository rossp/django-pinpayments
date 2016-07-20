from django.http import HttpResponse
from django.contrib.auth import get_user_model

from .models import CustomerToken
from .models import PinRecipient
from .models import PinTransaction
from .models import PinTransfer

def register_customer(request):
    customerToken = CustomerToken()
    customerToken.card_number = '5520000000000000'
    customerToken.card_name = 'Example Card'
    User = get_user_model()
    user = User.objects.get(email = 'rahul.sharma416@gmail.com')
    
    output = customerToken.create_from_card_token('card__tAqHdhvwmY2DiltiAoLow', user, 'test')
    return HttpResponse(output)

def charge_customer(request):
    pinTransaction = PinTransaction()
    
    pinTransaction.email_address = 'rahul.sharma416@gmail.com'
    pinTransaction.description = 'Services fee'
    pinTransaction.amount = 100
    pinTransaction.currency = 'AUD'
    pinTransaction.ip_address = get_client_ip(request)
    customerToken = CustomerToken.objects.get(token = 'cus_UetjXq4GewUZPSlkh9OCVw')
    pinTransaction.customer_token = customerToken
    
    output = pinTransaction.process_transaction()
    return HttpResponse(output)

def transfer_to_recipient(request):
    pinTransfer = PinTransfer()
    recipientToken = PinRecipient.objects.get(token = 'rp_O6KLV2QQ9SG5THvsp8w-Yg')
    
    output = pinTransfer.send_new(90, 'Services earning', recipientToken, 'AUD')
    return HttpResponse(output)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def register_recipient(request):
    pinRecipient = PinRecipient()
    
    output = pinRecipient.create_with_bank_account('roland@pin.net.au', 'Mr Roland Robot', '123456', '987654321', 'Mr Roland Robot')
    return HttpResponse(output)


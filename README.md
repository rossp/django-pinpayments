# django-pinpayments

`django-pinpayments` provides helper functions for [Pin Payments](https://pin.net.au) - a relatively new Australian payment processor that doesn't require merchant accounts and that doesn't require purchasers to have an account. Some may call it the "Australian version of Stripe".

`django-pinpayments` provides template tags to render the [*Pin.js payment form*](https://pin.net.au/docs/guides/payment-forms), which uses the Card API for processing. This means you can collect credit card details on your website, submit them via javascript to Pin (without them landing on your server), then process the payment on your server using the single-use card token that Pin return.

The provided Card tokens can also be used to create [Customer tokens](https://pin.net.au/docs/api/customers), to use for delayed or recurring billing.

`django-pinpayments` is designed to be a simple base for your own billing projects. It doesn't make too many assumptions, and leaves many things open for your design input.


### Not Included

* Any link to your existing models or business logic
* Views for users to review/update their stored credit cards, or review previous transactions

### Todo

* Tests
* More documentation
* Signals on success or failure

### Pre-requisites

* Django (Only tested on 1.4 & 1.5)
* [python-requests](http://docs.python-requests.org/en/latest/)
* [Mock](http://www.voidspace.org.uk/python/mock/)

### Settings

* `PIN_ENVIRONMENTS` - a dictionary of dictionaries containing Pin API keys & secrets
* `PIN_DEFAULT_ENVIRONMENT` - a pointer to the environment to be used at runtime, if no specific environment is requested.

**Warning:** Make sure your settings do not end up in public source repositories, as they can be used to process payments in your name. 

#### `PIN_ENVIRONMENTS`

Each environment must have the 'key' and 'secret' values. 

I highly recommend at least test & production, however you can also configure other key pairs if you have eg a separate Pin account for part of your website. Perhaps you have membership sales processed by one account, and merchandise by another. 

This setting, with at least one environment, is **required** for django-pinpayments to function. There is no default.

```python
    PIN_ENVIRONMENTS = {
        'test': {
            'key': 'pk_qokBvPpEHIVmNETSoSdDVYP',
            'secret': 'MBjZMurpDtjDANDNFQObZmBhMg',
            'host': 'test-api.pin.net.au',
        },
        'live': {
            'key': 'pk_yGCGLonMHJMFscFyNaLZdkEV',
            'secret': 'tOAQeMsMaBrxejJHIqHJVIObUS',
            'host': 'api.pin.net.au',
        },
        'live_project2' {
            'key': 'pk_ByNNmfJfsMywEIEa-aCteTR',
            'secret': 'CPslpGmoakWdPuxjtrfibZVLaS',
            'host': 'api.pin.net.au',
        },
    }
```

API keys and secrets are available from your [Pin Account page](https://dashboard.pin.net.au/account). Hosts should not include *https* or a trailing slash; these will be added automatically.

#### `PIN_DEFAULT_ENVIRONMENT`

At runtime, the `{% pin_headers %}` template tag can define which environment to use. If you don't specify an environment in the template tag, this setting determines which account to use.

**Default:** `PIN_DEFAULT_ENVIRONMENT = 'test'`

### Template Tags

Two template tags are included. One includes the Pin.js library and associated JavaScript, and the other renders a form that doesn't submit to your server. Both are required.

Both tags are in `pin_payments_tags`, so you should include `{% load pin_payments_tags %}` somewhere near the top of your template.

#### `pin_headers` - Render `pin.js` and helper functions

This tag should be called inside the `head` tag of your HTML page. It will render multiple `<script>` tags: one to load `pin.js`, the other to define a function that will run on submit of the form to load the card token from the Pin API.

```html
    {% load pin_payments_tags %}
    <html>
        <head>
            <title>My Payment Page</title>
            <script src='/path/to/jquery.js'></script>
            {% pin_headers "test" %}
        </head>
        <body>
            <!-- page content -->
        </body>
    </html>
```

The output of this tag can be overridden by modifying `templates/pinpayments/pin_headers.html`. The included sample utilises jQuery, which should be included in your page prior to the `pin_headers` template tag.

To switch to your live API tokens, change `test` to `live`.

#### `pin_form` - Render HTML form for Payment

Use `pin_form` to render the payment form, which includes billing address and credit card details. Your fpage should already include a form tag, the `pin_headers` tag, and the `csrf_token`. 

```html
    <form method='post' action='.' class='pin'>
        {% csrf_token %}
        <!-- your existing form -->
        {% pin_form %}
        <input type='submit' value='Process Payment'>
    </form>
```

By default, the template does not include `name` attributes on the fields so they will not be posted to your server. You can modify `templates/pinpayments/pin_form.html` to customise the form layout.

### Models

#### `pinpayments.PinTransaction`

This model holds attempted and processed payments, including full details of the API response from Pin.

There's an assumption that you'll have your own "Order" table, with a 1:N or N:N link to `PinTransaction`.

To create a new Transaction in the view that receives the form submission, use the PinTransaction model along with some custom data.

```python
    t = PinTransaction()
    t.card_token = request.POST.get('card_token')
    t.ip_address = request.POST.get('ip_address')
    t.amount = 500 # Amount in dollars. Define with your own business logic.
    t.currency = 'AUD' # Pin supports AUD and USD. Fees apply for currency conversion.
    t.description = 'Payment for invoice #12508' # Define with your own business logic
    t.email_address = request.user.email_address 
    t.save()

    result = t.process_transaction() # Typically "Success" or an error message
    if t.succeeded == True:
        return "We got the money!"
    else:
        return "No money today :( Error message: %s " % result
```

You may choose to call the `process_transaction()` function sometime *after* creation of the `PinTransaction`, for example from a cronjob or worker queue. This is left as an exercise for the reader.

#### pinpayments.CustomerToken

If you do recurring billing, or if you charge a card a significant amount of time after collecting card details (at present, Pin [expire card tokens](https://pin.net.au/docs/api/cards) after 1 month) then you need to use the Customers API to create a `Customer` record. A `Customer` can then have multiple transactions created, without collecting card details again.

In the view that receives `card_token` from your payment form, create a new instance of `CustomerToken` using the provided `create_from_card_token` function.

To allow users to manage their active cards, a `CustomerToken` record must be tied to a `contrib.auth.User` record. You should provide a view to review & cancel `CustomerToken` records.

```python
    card_token = request.POST.get('card_token')
    user = request.user
    customer = CustomerToken.create_from_card_token(card_token, user, environment='test')
```

If you later want to charge this customer, just create a new `PinTransaction` for them.

```python
    # Get the first active token. Big assumption that we have one we can use.
    customer = request.user.customertoken_set.filter(active=True)[0]
    transaction = PinTransaction(
        customer_token  = customer,
        email           = request.user.email,
        ip_address      = request.META.get('REMOTE_ADDR'),
        amount          = 25, # Dollars
        currency        = 'AUD',
        description     = 'Monthly payment',
    )
    transaction.save()
    result = transaction.process_transaction()
    if t.succeeded == True:
        return "We got the money!"
    else:
        return "No money today :( Error message: %s " % result
    )
```
   
Because you're keeping the `CustomerToken`, you can re-bill them as often as is necessary (within your legal rights and your agreement with the customer, obviously). 

### Warnings

I'm not responsible for anything this code does to your customers, your bank account, or your Pin account. I am providing it in good faith and provide no warranties.  The above code samples are just that: Samples. Your production code should be full of testing and other ways to deal with the many errors and problems that arise from processing payments online.

All use is at your own risk. 

### Contributing

I'd love to improve this library. Please log issues and pull requests via GitHUb.

### License

Copyright (c) 2013, Ross Poulton <ross@rossp.org>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

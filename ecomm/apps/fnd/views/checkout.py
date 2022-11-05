from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.translation import get_language
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import (
    get_object_or_404, 
    render,
    redirect,
)
from django.contrib import messages
from ecomm.apps.fnd.models import (
    Delivery,
    Order,
    OrderProduct,
)
import json
from ecomm.apps.fnd.utils.cart import Cart


@require_http_methods(['GET'])
def index(request):
    # Cart in fhd.context.common
    return render(request, 'apps/fnd/checkout.html', {})


#@login_required
@require_http_methods(['POST'])
def update_delivery(request):
    cart = Cart(request)
    result = json.loads(request.body)
    delivery_id = int(result['id'])
    if delivery_id != 0:
        delivery = get_object_or_404(Delivery.objs.fnd().valid().shown(), id=delivery_id)
        cart_total = cart.update_delivery(delivery.price)
        delivery_price = delivery.price
        cart.add_delivery(delivery.id)
    else:
        cart.clear('purchase')
        cart_total = cart.update_delivery()
        delivery_price = 0.0

    return JsonResponse({
        'total_price': cart_total,
        'delivery_price': delivery_price,
    })

# ###
# PayPay
# ###
from paypalcheckoutsdk.orders import OrdersGetRequest
from ecomm.apps.fnd.utils.paypal import PayPalClient
from paypalhttp import HttpError


# @login_required
@require_http_methods(['POST'])
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body['orderID']
    buyer_data = body['buyerData']
    account_id = None

    if request.user.is_authenticated:
        account_id = request.user.id

    try:
        requestorder = OrdersGetRequest(data)
        response = PPClient.client.execute(requestorder)

        total_paid = response.result.purchase_units[0].amount.value
        email = buyer_data['email'] if buyer_data['email'] else response.result.payer.email_address
        address = buyer_data['address'] if buyer_data['address'] else response.result.purchase_units[0].shipping.address.address_line_1
        postal_code = buyer_data['post'] if buyer_data['post'] else response.result.purchase_units[0].shipping.address.postal_code
        country_code = buyer_data['country'] if buyer_data['country'] else response.result.purchase_units[0].shipping.address.country_code
        order_key = response.result.id

        # full_name=response.result.purchase_units[0].shipping.name.full_name,
        # email=response.result.payer.email_address,
        # address=response.result.purchase_units[0].shipping.address.address_line_1,
        # postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        # country_code=response.result.purchase_units[0].shipping.address.country_code,

        cart = Cart(request)
        order = Order.objs.create(
            account_id=account_id,
            email=email,
            address=address,
            postal_code=postal_code,
            country_code=country_code,
            total_paid=total_paid,
            order_key=order_key,
            payment='paypal',
            billing_status=True,
            is_shown=True,
            fnd_id=settings.FND_ALIAS,
        )
        order_id = order.pk

        for item in cart:
            OrderProduct.objs.create(
                order_id=order_id, 
                product_id=item['product']['id'], 
                price=item['price'], 
                quantity=item['quantity'],
                fnd_id=settings.FND_ALIAS,
            )
        return JsonResponse('Payment completed!', safe=False, status=200)
    except:
        return JsonResponse('Payment completed!', safe=False, status=500)

    

#@login_required
def payment_successful(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, _('Successful payment'))
    return redirect('fnd:home')

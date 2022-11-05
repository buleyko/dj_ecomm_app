from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import ( 
    get_object_or_404, 
    render,
    redirect,
)
import json
from ecomm.apps.fnd.utils.cart import Cart
from ecomm.apps.fnd.models import (
    Product,
    Order,
    Delivery,
)



@require_http_methods(['GET'])
def index(request):
    current_language = get_language()
    deliveries = Delivery.objs.fnd().valid().shown()
    return render(request, 'apps/fnd/cart.html', {
        'deliveries': deliveries,
    })
 
    
    return redirect('account:dashboard')

@require_http_methods(['POST'])
def add(request):
    cart = Cart(request)
    result = json.loads(request.body)
    item_id = int(result['id'])
    item_quantity = int(result['quantity'])
    product = get_object_or_404(Product, id=item_id)
    cart.add(product=product, quantity=item_quantity)
    cart_filling = len(cart)
    return JsonResponse({'quantity': cart_filling})


@require_http_methods(['POST'])
def update(request):
    cart = Cart(request)
    result = json.loads(request.body)
    item_id = int(result['id'])
    item_quantity = int(result['quantity'])
    cart.update(product=item_id, quantity=item_quantity)
    cart_filling = len(cart)
    cart_total = cart.get_total_price()
    prod_quantity = cart.get_product_quantity(item_id)
    prod_total_price = cart.get_product_total_price(item_id)
    return JsonResponse({
        'id': item_id,
        'quantity': cart_filling, 
        'total_price': cart_total,
        'prod_quantity': prod_quantity,
        'prod_total_price': prod_total_price,
    })


@require_http_methods(['POST'])
def delete(request):
    cart = Cart(request)
    result = json.loads(request.body)
    item_id = int(result['id'])
    cart.delete(product=item_id)
    cart_filling = len(cart)
    cart_total = cart.get_total_price()
    return JsonResponse({
        'id': item_id, 
        'quantity': cart_filling, 
        'total_price': cart_total,
    })
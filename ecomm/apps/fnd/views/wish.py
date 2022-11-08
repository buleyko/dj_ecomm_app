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
from ecomm.apps.fnd.utils.wish import Wish
from ecomm.apps.fnd.models import (
    Product,
    ProductBaseTranslation,
    ProductTypeAttribute,
)


@require_http_methods(['GET'])
def index(request):
    # Wish in fhd.context.common
    return render(request, 'apps/fnd/wish.html', {})


@require_http_methods(['POST'])
def add(request):
    wish = Wish(request)
    result = json.loads(request.body)
    item_id = int(result['id'])
    product = get_object_or_404(Product, id=item_id)
    wish.add(product.id)
    wish_filling = len(wish)
    if request.user.is_authenticated:
        request.user.update_wish(product.id, 'add')
    return JsonResponse({'quantity': wish_filling})


@require_http_methods(['POST'])
def delete(request):
    wish = Wish(request)
    result = json.loads(request.body)
    item_id = int(result['id'])
    product = get_object_or_404(Product, id=item_id)
    wish.delete(product.id)
    wish_filling = len(wish)
    if request.user.is_authenticated:
        request.user.update_wish(product.id, 'remove')
    return JsonResponse({'quantity': wish_filling})
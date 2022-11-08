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
from ecomm.apps.fnd.utils.comparison import Comparison
from ecomm.apps.fnd.models import (
    Product,
    ProductBaseTranslation,
    ProductTypeAttribute,
)


@require_http_methods(['GET'])
def index(request):
    # Comparison in fhd.context.common
    return render(request, 'apps/fnd/compare.html', {})


@require_http_methods(['POST'])
def add(request):
    comparison = Comparison(request)
    result = json.loads(request.body)
    item_id = int(result['id'])
    product = get_object_or_404(Product, id=item_id)
    comparison.add(product.id)
    comparison_filling = len(comparison)
    if request.user.is_authenticated:
        request.user.update_comparison(product.id, 'add')
    return JsonResponse({'quantity': comparison_filling})


@require_http_methods(['POST'])
def delete(request):
    comparison = Comparison(request)
    result = json.loads(request.body)
    item_id = int(result['id'])
    product = get_object_or_404(Product, id=item_id)
    comparison.delete(product.id)
    comparison_filling = len(comparison)
    if request.user.is_authenticated:
        request.user.update_comparison(product.id, 'remove')
    return JsonResponse({'quantity': comparison_filling})
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from ecomm.vendors.helpers.pagination import with_pagination
from django.conf import settings
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import ( 
    get_object_or_404, 
    render,
    redirect,
)
import json
from django.db.models import F
from ecomm.apps.fnd.utils.cart import Cart
from ecomm.vendors.helpers.request import (
    get_filter_arguments,
    get_search_arguments,
)
from ecomm.apps.fnd.models import (
    Category,
    ProductType,
    Product,
    ProductTypeAttribute,
)

@require_http_methods(['GET'])
def products(request, type_slug):
    current_language = get_language()
    filter_arguments = get_filter_arguments(request)
    search_arguments = get_search_arguments(request)

    prod_type = ProductType.objs.fnd().valid().shown().\
        select_related('category').\
        filter(slug=type_slug).\
        first()
    if prod_type is None:
        raise Http404

    attrs = ProductTypeAttribute.objs.filter(prod_type__slug=type_slug).\
        values(
            slug=F('prod_attribute__slug'), 
            tr=F('prod_attribute__name')
        ).distinct()

    attr_values = Product.objs.fnd().valid().shown().order_by().\
        filter(is_default=True).\
        filter(product_type=prod_type).\
        values(
            attr_slug=F('attribute_values__product_attribute__slug'),
            val=F('attribute_values__value'),
            tr=F('attribute_values__trs')
        ).distinct()

    products = Product.objs.valid().shown().\
        filter(is_default=True).\
        filter(product_type=prod_type).\
        filter_in_if_args_exists('attribute_values__value__in', filter_arguments).\
        filter_contains_if_args_exists('full_name__icontains', search_arguments).\
        select_related('prod_base').\
        distinct()


    return render(request, 'apps/fnd/type.html', {
        'page_obj': with_pagination(request, products),
        'prod_type': prod_type,
        'attrs': attrs,
        'attr_values': attr_values,
        'filter_arguments': filter_arguments,
        'search_arguments': search_arguments,
    })
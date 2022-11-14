from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from ecomm.vendors.helpers.pagination import with_pagination
from django.db.models import Prefetch
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
    Product,
    ProductType,
    ProductTypeAttribute,
)

@require_http_methods(['GET'])
def products(request, cat_slug):
    current_language = get_language()
    filter_arguments = get_filter_arguments(request)
    search_arguments = get_search_arguments(request)

    category = Category.objs.fnd().valid().shown().\
        filter(slug=cat_slug).\
        prefetch_related(
            Prefetch('types', 
                queryset=ProductType.objs.valid(), 
            )
        ).first()
    if category is None:
        raise Http404

    attrs = ProductTypeAttribute.objs.valid().shown().\
        filter(prod_type__prod__prod_base__category__slug=cat_slug).\
        values(
            slug=F('prod_attribute__slug'), 
            tr=F('prod_attribute__name')
        ).distinct()

    attr_values = Product.objs.fnd().valid().shown().order_by().\
        filter(is_default=True).\
        filter(
            prod_base__category__in=Category.objs.get(slug=cat_slug).get_descendants(include_self=True)
        ).\
        values(
            attr_slug=F('attribute_values__product_attribute__slug'),
            val=F('attribute_values__value'),
            tr=F('attribute_values__trs')
        ).distinct()

    products = Product.objs.valid().shown().\
        filter(is_default=True).\
        filter(
            prod_base__category__in=Category.objs.get(slug=cat_slug).get_descendants(include_self=True)
        ).\
        filter_in_if_args_exists('attribute_values__value__in', filter_arguments).\
        filter_contains_if_args_exists('full_name__icontains', search_arguments).\
        select_related('prod_base').\
        distinct()

    return render(request, 'apps/fnd/category.html', {
        'page_obj': with_pagination(request, products),
        'category': category,
        'attrs': attrs,
        'attr_values': attr_values,
        'filter_arguments': filter_arguments,
        'search_arguments': search_arguments,
    })
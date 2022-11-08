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
from django.db.models import F
from ecomm.apps.fnd.utils.cart import Cart
from ecomm.apps.fnd.models import (
    Category,
    Product,
    ProductTypeAttribute,
)


@require_http_methods(['GET'])
def show(request, prod_slug):
    current_language = get_language()
    product = Product.objs.fnd().valid().shown().\
        filter(slug=prod_slug).\
        prefetch_related('media').\
        select_related('prod_base').\
        first()
    if product is None:
        raise Http404

    attrs = ProductTypeAttribute.objs.filter(prod_type__prod__slug=product.slug).\
        values(
            slug=F('prod_attribute__slug'), 
            name=F('prod_attribute__name')
        ).distinct()

    attr_values = Product.objs.fnd().valid().shown().filter(is_default=True).\
        filter(slug=product.slug).\
        values(
            attr_slug=F('attribute_values__product_attribute__slug'),
            val=F('attribute_values__value'),
            tr=F('attribute_values__trs')
        ).distinct()

    return render(request, 'apps/fnd/product.html', {
        'product': product,
        'attrs': attrs,
        'attr_values': attr_values,
    })

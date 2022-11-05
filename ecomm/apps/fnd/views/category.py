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
    Category,
    Product,
    ProductTypeAttribute,
)

@require_http_methods(['GET'])
def show(request, cat_slug):
    current_language = get_language()
    filter_arguments = get_filter_arguments(request)
    search_argument = get_search_argument(request)

    category = Category.objs.fnd().valid().shown().filter(slug=_id).\
        prefetch_translation_by(
            CategoryTranslation, 
            current_language,
            defers=CategoryTranslation.defer_values
        ).first()
    if category is None:
        raise Http404


    attrs = ProductTypeAttribute.objs.filter(prod_type__prod__prod_base__category__slug=cat_slug).\
        values(
            slug=F('prod_attribute__slug'), 
            tr=F('prod_attribute__trs')
        ).distinct()

    attr_values = Product.objs.fnd().valid().shown().filter(is_default=True).\
        filter(prod_base__category__in=Category.objs.get(slug=cat_slug).get_descendants(include_self=True)).\
        values(
            attr_slug=F('attribute_values__product_attribute__slug'),
            val=F('attribute_values__value'),
            tr=F('attribute_values__trs')
        ).distinct()

    products = Product.objs.valid().shown().filter(is_default=True).\
        filter_in_if_args_exists('attribute_values__value__in', filter_arguments).\
        filter_contains_if_arg_exist(
            [
                'prod_base__title__contains', 
                ('prod_base__translation__name__contains', 'or',)
            ], search_argument
        ).\
        filter(prod_base__category__in=Category.objs.get(slug=cat_slug).get_descendants(include_self=True)).\
        order_by('-created_at').\
        select_related('prod_base').\
        prefetch_related(
            Prefetch('prod_base__translation', 
                queryset=ProductBaseTranslation.objs.filter(lang_id=current_language).\
                    defer(*ProductBaseTranslation.defer_values), 
                to_attr='tr'
            )
        ).distinct()

    page_obj = with_pagination(request, products)

    return render(request, 'apps/fnd/category.html', {
        'page_obj': with_pagination(request, products),
        'category': category,
        'attrs': attrs,
        'attr_values': attr_values,
        'filter_arguments': filter_arguments,
        'search_argument': search_argument,
    })
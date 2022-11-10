from django.views.decorators.http import require_http_methods
from ecomm.vendors.helpers.pagination import with_pagination
from django.http import JsonResponse
from django.conf import settings
import json
from ecomm.vendors.helpers.request import (
    get_filter_arguments,
    get_search_arguments,
)
from django.shortcuts import (
    render,
    redirect,
)
from django.utils.translation import get_language
from ecomm.apps.fnd.models import (
    Fnd,
    Product,
)



@require_http_methods(['GET'])
def home(request):
    search_arguments = get_search_arguments(request)

    products = Product.objs.fnd().valid().shown().\
        filter(is_default=True).\
        filter_contains_if_args_exists('full_name__icontains', search_arguments).\
        select_related('prod_base')
        
    return render(request, 'apps/fnd/home.html', {
        'page_obj': with_pagination(request, products),
        'search_arguments': search_arguments,
    })


@require_http_methods(['POST'])
def options(request):
    ''' change theme and content_layout  '''
    options = request.session.get('options')
    if 'options' not in request.session:
        options = request.session['options'] = {}

    result = json.loads(request.body)
    settings = result['settings']

    for param in settings:
        options[param['key']] = param['val']
    request.session.modified = True

    return JsonResponse({
        'options': options,
    })


@require_http_methods(['GET'])
def change_language(request, lang=settings.LANGUAGE_CODE):
    if lang in settings.LANGUAGE_CODES:
        request.session['lang'] = lang
    return redirect(request.META.get('HTTP_REFERER'))



# -------------- ERROR PAGES ----------------

@require_http_methods(['GET'])
def error_404(request, *args, **argv):
    data = {}
    return render(request,'apps/fnd/error/404.html', data)

def error_500(request, *args, **argv):
    data = {}
    return render(request,'apps/fnd/error/500.html', data)

def error_403(request, *args, **argv):
    data = {}
    return render(request,'apps/fnd/error/403.html', data)

def error_400(request, *args, **argv):
    data = {}
    return render(request,'apps/fnd/error/400.html', data)


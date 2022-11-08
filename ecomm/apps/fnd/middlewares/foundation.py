from termcolor import colored
from django.conf import settings
from django.utils.translation import get_language
from django.core.exceptions import PermissionDenied
from django.http import Http404
from ecomm.apps.fnd.models import Fnd


def foundation_middleware(get_response):
    
    def middleware(request):
        # fnd = Fnd.objs.valid().filter(alias=settings.FND_ALIAS).first()
        # if fnd is None:
        #     raise Http404
        # request.fnd = fnd

        response = get_response(request)

        return response

    return middleware
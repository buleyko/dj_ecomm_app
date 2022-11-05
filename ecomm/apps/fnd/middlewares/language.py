from django.utils.translation import get_language
from django.utils import translation


def language_middleware(get_response):
    
    def middleware(request):
        if request.session.get('lang', False):
            lang = request.session['lang']
        else:
            lang = get_language()
        translation.activate(lang)
        response = get_response(request)
        translation.deactivate()

        return response

    return middleware
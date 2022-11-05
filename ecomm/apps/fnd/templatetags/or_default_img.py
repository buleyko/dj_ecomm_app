from django import template
from django.templatetags.static import static
from django.conf import settings

register = template.Library()

@register.filter(name='or_default_img')
def or_default_img(value, key='PLACEHOLDER'):
    ''' set default image by key, for imagefield in values '''
    default_img = settings.DEFAULT_IMAGE[key]
    try:
        return static(default_img) if not value else f'{settings.MEDIA_URL}{value}'
    except:
        return static(default_img)
from django import template

register = template.Library()

@register.filter(name='by_lang')
def by_lang(value, key):
	try:
		return value[key]
	except:
		return None
from django import template

register = template.Library()

@register.filter(name='by_lang')
def by_lang(value, key):
	try:
		if value.get(str(key), False):
			return value[key]
		elif value.get('title', False):
			return value['title']
		else:
			return None
	except:
		return None
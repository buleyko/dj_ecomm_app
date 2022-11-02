from django.core.paginator import Paginator
from django.conf import settings

def with_pagination(request, objs):
	paginator = Paginator(objs, settings.NUMBER_PER_PAGE)
	page_number = request.GET.get('page')
	return paginator.get_page(page_number)
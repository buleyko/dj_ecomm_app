

def get_filter_arguments(request):
	filter_arguments = []
	if request.GET:
		for key, val in request.GET.lists():
			if 'search-' not in key:
				filter_arguments = [*filter_arguments, *val]
	return filter_arguments 


def get_search_arguments(request):
	search_argument = ''
	if request.GET:
		for key, val in request.GET.lists():
			if 'search-' in key:
				search_argument = [*search_argument, *val]
	return search_argument
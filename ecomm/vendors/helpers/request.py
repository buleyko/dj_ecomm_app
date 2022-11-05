

def get_filter_arguments(request):
	filter_arguments = []
	if request.GET:
		for key, val in request.GET.items():
			if 'search-' not in key:
				filter_arguments.append(val)
	return filter_arguments 


def get_search_argument(request):
	search_argument = ''
	if request.GET:
		for key, val in request.GET.items():
			if 'search-' in key:
				search_argument = str(val)
	return search_argument
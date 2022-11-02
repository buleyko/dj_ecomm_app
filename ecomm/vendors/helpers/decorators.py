from functools import wraps
from django.shortcuts import redirect
from django.conf import settings


def redirect_if_authenticated(redirect_to=settings.REDIRECT_TO_IF_AUTHENTICATED):
	''' If User is authenticated redirect to ... '''
	def decorator(view_func):
		@wraps(view_func)
		def wrapper(request, *args, **kwargs):
			if request.user.is_authenticated:
				return redirect(redirect_to)
			return view_func(request, *args, **kwargs)
		return wrapper
	return decorator
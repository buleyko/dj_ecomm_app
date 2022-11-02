from termcolor import colored
from django.conf import settings
from django.utils.translation import get_language
from django.core.exceptions import PermissionDenied
from django.http import Http404
from ecomm.apps.fnd.models import (
	Fnd,
)
# from ecomm.apps.fnd.utils import (
# 	Cart, 
# 	Wish, 
# 	Comparison,
# )


def context_processor(request):
	current_language = get_language()
	
	return {
		'fnd': None,
	}
from termcolor import colored
from django.conf import settings
from django.utils.translation import get_language
from django.core.exceptions import PermissionDenied
from django.http import Http404
from ecomm.apps.fnd.models import (
	Fnd,
	Category,
)
from ecomm.apps.fnd.utils import (
	Cart, 
	Wish, 
	Comparison,
)


def context_processor(request):
	cart = Cart(request)
	wish = Wish(request)
	comparison = Comparison(request)

	fnd = Fnd.objs.valid().filter(alias=settings.FND_ALIAS).first()
	if fnd is None:
		print(colored('\nfoundation not exist', 'red'))
		print(colored('set settings.FND_ALIAS=<alias>\nand run command: create_foundation <alias>\n', 'green'))
		raise Http404

	categories = Category.objs.fnd().valid()

	options = fnd.set_options(request.session)
	
	return {
		'fnd': fnd,
		'categories': categories,
		'options': options,
		'cart': cart,
		'wish': wish,
		'comparison': comparison,
	}
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from ecomm.vendors.helpers.pagination import with_pagination
from django.conf import settings
from django.contrib import messages
from django.shortcuts import (
	render, 
	redirect,
)
from django.db.models import Sum
from ecomm.apps.fnd.models import (
	Order,
	OrderProduct,
)
from django.contrib.auth import get_user_model
Account = get_user_model()


@login_required
@require_http_methods(['GET'])
def dashboard(request):
	current_language = get_language()
	return render(request, 'apps/account/dashboard.html', {})


@login_required
@require_http_methods(['GET'])
def orders(request):
	orders = Order.objs.fnd().valid().\
		filter(account_id=request.user.id).filter(billing_status=True).\
		order_by('-created_at').\
		prefetch_related('order_orderprods').\
		annotate(total_amount=Sum('order_orderprods__quantity'))
		
	page_obj = with_pagination(request, orders)
	return render(request, 'apps/account/orders.html', {
		'page_obj': page_obj,
	})
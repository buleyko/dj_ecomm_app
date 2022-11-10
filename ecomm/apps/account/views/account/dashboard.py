from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.contrib import messages
from ecomm.apps.fnd.models import Order
from django.shortcuts import (
	render, 
	redirect,
)
from django.contrib.auth import get_user_model
Account = get_user_model()


@login_required
@permission_required('account.view_dashboard', raise_exception=True)
@require_http_methods(['GET'])
def index(request):
	number_of_orders = Order.objs.fnd().valid().\
		filter(account_id=request.user.id).\
		filter(billing_status=True).\
		count()
	return render(request, 'apps/account/dashboard.html', {
		'number_of_orders': number_of_orders,
	})
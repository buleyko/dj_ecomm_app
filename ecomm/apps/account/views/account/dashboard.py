from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.shortcuts import (
	render, 
	redirect,
)
from django.contrib.auth import get_user_model
Account = get_user_model()


@login_required
@require_http_methods(['GET'])
def dashboard(request):
	current_language = get_language()
	return render(request, 'apps/account/dashboard.html', {})
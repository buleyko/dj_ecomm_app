from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from ecomm.vendors.helpers.decorators import redirect_if_authenticated
from django.contrib.auth.decorators import permission_required
from ecomm.vendors.helpers.token import account_token
from ecomm.apps.fnd.tasks.mail import send_email_celery_task
from ecomm.vendors.helpers.pagination import with_pagination
from django.conf import settings
from django.contrib import messages
from django.shortcuts import (
	render, 
	redirect,
)
from django.db.models import Sum
from ecomm.vendors.helpers.mail import get_reset_passwd_mail_body
from ecomm.apps.account.forms.account import (
	PwdResetForm,
	PwdResetConfirmForm,
)
from django.contrib.auth import get_user_model
Account = get_user_model()



@require_http_methods(['GET', 'POST'])
def reset_passwd(request):
	if request.method == 'POST':
		form = PwdResetForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			user = Account.objs.get(email=email)

			send_email_celery_task.delay(user.email, get_reset_passwd_mail_body(request, user))

			messages.success(request, _('Message: Mail send'))
			return redirect('fnd:home')
		else:
			form = PwdResetForm(request.POST)
			return render(request, 'apps/account/passwd_reset.html', {
				'form': form,
			})
	if request.method == 'GET':
		form = PwdResetForm()
		return render(request, 'apps/account/passwd_reset.html', {
			'form': form,
		})


@require_http_methods(['GET', 'POST'])
def confirm_passwd(request):
	if request.method == 'POST':
		user = Account.get_by_uid(request.session['user_uid'])
		if user is not None:
			form = PwdResetConfirmForm(user, request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, _('Message: passwd changed'))
				del request.session['user_uid']
				return redirect('fnd:home')
			else:
				form = PwdResetConfirmForm(user, request.POST)
				return render(request, 'apps/account/passwd_confirm.html', {
					'form': form,
				})
		else:
			messages.success(request, _('Message: user is None'))
			return redirect('fnd:home')

	if request.method == 'GET':
		user = Account.get_by_uid(request.session['user_uid'])
		if user is not None:
			form = PwdResetConfirmForm(user)
			return render(request, 'apps/account/passwd_confirm.html', {
				'form': form,
			})
		else:
			messages.success(request, _('Message: user is None'))
			return redirect('fnd:home')

@require_http_methods(['GET'])
def confirm_passwd_mail(request, uidb64, token):
	user = Account.get_by_uid(uidb64)
	if user is not None and account_token.check_token(user, token):
		request.session['user_uid'] = uidb64
		return redirect('account:confirm_passwd')
	else:
		messages.success(request, _('Message: invalid get user by tiken'))
		return redirect('fnd:home')
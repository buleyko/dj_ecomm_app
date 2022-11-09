from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from ecomm.vendors.helpers.decorators import redirect_if_authenticated
from django.contrib.auth.decorators import permission_required
from ecomm.vendors.helpers.token import account_token
from ecomm.vendors.helpers.mail import get_activate_account_mail_body
from ecomm.apps.fnd.tasks.mail import send_email_celery_task
from django.http import HttpResponse
from django.contrib import messages
import logging
from django.contrib.auth import (
    login, 
    logout, 
    authenticate,
)
from django.shortcuts import ( 
    get_object_or_404, 
    render,
    redirect,
)
from ecomm.apps.account.forms.auth import (
    AccountRegistrationForm,
    AccountLoginForm,
)
from django.contrib.auth import get_user_model
Account = get_user_model()

logger = logging.getLogger("main")


@redirect_if_authenticated()
@require_http_methods(['GET'])
def signin(request):
    loginForm = AccountLoginForm(
        initial={'next_url': request.GET.get('next')}
    )
    return render(request, 'apps/account/auth/login.html', {
        'form': loginForm,
    })


@redirect_if_authenticated()
@require_http_methods(['POST'])
def entry(request):
    loginForm = AccountLoginForm(request.POST)
    if loginForm.is_valid():
        email = loginForm.cleaned_data['email']
        password = loginForm.cleaned_data['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            user.is_active = True
            user.save()
            if request.POST['next_url']:
                return redirect(request.POST['next_url'])
            return redirect('account:dashboard')
        else:
            messages.error(request, _('Error authenticate user'))
            return render(request, 'apps/account/auth/login.html', {
                'form': loginForm,
            })
    else:
        return render(request, 'apps/account/auth/login.html', {
            'form': loginForm,
        })


@redirect_if_authenticated()
@require_http_methods(['GET'])
def signup(request):
    registerForm = AccountRegistrationForm()
    return render(request, 'apps/account/auth/register.html', {
        'form': registerForm,
    })


@redirect_if_authenticated()
@require_http_methods(['POST'])
def registration(request):
    registerForm = AccountRegistrationForm(request.POST)
    if registerForm.is_valid():
        user = registerForm.save(commit=False)
        user.email = registerForm.cleaned_data['email']
        user.set_password(registerForm.cleaned_data['password'])
        user.is_active = False
        user.save()
        logger.info(f'REGISTRATION USER: {user.id}')

        # send registration email
        try:
            send_email_celery_task.delay(user.email, get_activate_account_mail_body(request, user))
        except:
            pass

        messages.success(request, _('Accaunt created. For activation check mail'))
        return redirect('fnd:home')
    else:
        return render(request, 'apps/account/auth/register.html', {
            'form': registerForm,
        })


@login_required
def signout(request):
    user = Account.objs.get(email=request.user.email)
    user.is_active = False
    user.save()
    logout(request)
    logger.info(f'LOGOUT USER: {user.id}')
    return redirect('fnd:home')


@redirect_if_authenticated()
@require_http_methods(['GET'])
def account_activate(request, uidb64, token):
    user = Account.get_by_uid(uidb64)
    if user is not None and account_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('account:dashboard')
    else:
        messages.success(error, 'Message: Invalid activation account')
        return redirect('fnd:home')
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .token import account_token
from django.core.mail import send_mail
from django.conf import settings


def get_uid_and_token(user):
	return {
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': account_token.make_token(user),
	}

def get_mail_body(request, user, template, subject='', uid_and_token=False, **kwargs):
	current_site = get_current_site(request)
	subject = f'{current_site.domain}: {subject}'
	data = {
		'user':user, 
		'domain': current_site.domain,
		**kwargs,
	}
	if uid_and_token:
		data = {**data, **get_uid_and_token(user)}

	return render_to_string(template, data)


def get_activate_account_mail_body(request, user):
	mail_body = get_mail_body(
		request, 
		user, 
		'src/mail/registration.html', 
		subject='Activate your Account', 
		uid_and_token=True,
	)
	return mail_body


def get_reset_passwd_mail_body(request, user):
	mail_body = get_mail_body(
		request, 
		user, 
		'src/mail/reset_passwd.html', 
		subject='Reset password', 
		uid_and_token=True,
	)
	return mail_body



def sender(user_email, subject, message):
	send_mail(
		subject, 
		message, 
		settings.ADMIN_EMAIL, 
		[user_email], 
		fail_silently=False
	)
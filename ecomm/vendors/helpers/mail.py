from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .token import account_token
from django.core.mail import send_mail
from django.conf import settings
from pathlib import Path


def get_mail_template(file):
	template_file = Path(settings.BASE_DIR + file)
	if template_file.is_file():
    	return file
    else:
    	path_list = file.split('/')
    	file_name = path_list.pop().split('_')
    	return '/'.join(path_list) + '/' + settings.LANGUAGE_CODE + '_' + file_name[1]


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


# def get_activate_account_mail_body(request, user):
# 	mail_body = get_mail_body(
# 		request, 
# 		user, 
# 		'src/mail/registration/en_registration.html', 
# 		subject=_('Activate your Account'), 
# 		uid_and_token=True,
# 	)
# 	return mail_body


# def get_reset_passwd_mail_body(request, user):
# 	mail_body = get_mail_body(
# 		request, 
# 		user, 
# 		'src/mail/reset_passwd/en_reset_passwd.html', 
# 		subject=_('Reset password'), 
# 		uid_and_token=True,
# 	)
# 	return mail_body


def get_activate_account_mail_body(request, user):
	try:
		template_file = get_mail_template('src/mail/registration/en_registration.html')
		mail_body = get_mail_body(
			request, 
			user, 
			template_file, 
			subject=_('Activate your Account'), 
			uid_and_token=True,
		)
		return mail_body
	except:
		pass


def get_reset_passwd_mail_body(request, user):
	try:
		template_file = get_mail_template('src/mail/reset_passwd/en_reset_passwd.html') 
		mail_body = get_mail_body(
			request, 
			user, 
			template_file, 
			subject=_('Reset password'), 
			uid_and_token=True,
		)
		return mail_body
	except:
		pass


def sender(user_email, subject, message):
	send_mail(
		subject, 
		message, 
		settings.ADMIN_EMAIL, 
		[user_email], 
		fail_silently=False
	)
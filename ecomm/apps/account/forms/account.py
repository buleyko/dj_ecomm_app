from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.helpers.validators import email_validation_check
from django.contrib.auth.forms import (
	PasswordResetForm,
	SetPasswordForm,
)
from ecomm.apps.account.models import Account


class PwdResetForm(PasswordResetForm):
	email = forms.EmailField(
		max_length=254,
		widget=forms.TextInput(
			attrs={'class': 'border border-color radius-2 p-4', 'placeholder': _('Email'), 'id': 'form-email'}
		))
	def clean_email(self):
		email = self.cleaned_data['email']
		email_validation_check(email)
		u = Account.objs.filter(email=email)
		if not u:
			raise forms.ValidationError(
				_('Unfortunatley we can not find that email address'))
		return email


class PwdResetConfirmForm(SetPasswordForm):
	new_password1 = forms.CharField(
		label=_('New password'), 
		widget=forms.PasswordInput(
			attrs={'class': 'border border-color radius-2 p-4', 'placeholder': _('New Password'), 'id': 'form-newpass'}
		))
	new_password2 = forms.CharField(
		label=_('Repeat password'), 
		widget=forms.PasswordInput(
			attrs={'class': 'border border-color radius-2 p-4', 'placeholder': _('New Password'), 'id': 'form-new-pass2'}
		))

	def clean_new_password2(self):
		new_passwd1 = self.cleaned_data['new_password1']
		new_passwd2 = self.cleaned_data['new_password2']
		if new_passwd1 != new_passwd2:
			raise forms.ValidationError(
				_('Passwords are not equal'))
		return new_passwd1
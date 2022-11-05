from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check
)
from django.contrib.auth.forms import (
	AuthenticationForm, 
	PasswordResetForm,
	SetPasswordForm
)
from ecomm.apps.account.models import Account


class AccountLoginForm(forms.Form):
	email = forms.EmailField(
		max_length=120
	)
	password = forms.CharField(
		widget=forms.PasswordInput()
	)
	next_url = forms.CharField(
		widget=forms.HiddenInput(), 
		required=False
	)

	def clean_password(self):
		passwd = self.cleaned_data['password']
		passwd_validation_check(passwd, _('Not valid password'))
		return passwd

	def clean_email(self):
		email = self.cleaned_data['email']
		email_validation_check(email, _('Not valid email'))
		return email

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['email'].widget.attrs.update(
	# 		{'class': 'form-input', 'placeholder': _('E-mail'), 'name': 'email'}
	# 	)
	# 	self.fields['password'].widget.attrs.update(
	# 		{'class': 'form-input', 'placeholder': _('Password'), 'name': 'password'}
	# 	)


class AccountRegistrationForm(forms.ModelForm):

	username = forms.CharField(
		label='Username', 
		min_length=4, 
		max_length=20, 
		help_text='Required'
	)
	email = forms.EmailField(
		max_length=100, 
		help_text='Required', 
		error_messages={
			'required': 'Sorry, you will need an email'
		}
	)
	password = forms.CharField(
		label='Password', 
		widget=forms.PasswordInput
	)
	password2 = forms.CharField(
		label='Repeat password', 
		widget=forms.PasswordInput
	)

	class Meta:
		model = Account
		fields = ('username', 'email',)

	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		r = Account.objs.filter(username=username)
		if r.count():
			raise forms.ValidationError("Username already exists")
		return username

	def clean_password(self):
		passwd = self.cleaned_data['password']
		passwd_validation_check(passwd, _('Not valid password'))
		return passwd

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError(_('Passwords do not match.'))
		return cd['password']

	def clean_email(self):
		email = self.cleaned_data['email']
		if Account.objs.filter(email=email).exists():
			raise forms.ValidationError(
				'Please use another Email, that is already taken')
		return email

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['username'].widget.attrs.update(
	# 		{'class': '', 'placeholder': 'Username'})
	# 	self.fields['email'].widget.attrs.update(
	# 		{'class': '', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
	# 	self.fields['password'].widget.attrs.update(
	# 		{'class': '', 'placeholder': 'Password'})
	# 	self.fields['password2'].widget.attrs.update(
	# 		{'class': '', 'placeholder': 'Repeat Password'})
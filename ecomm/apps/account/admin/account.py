from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from ecomm.apps.account.forms.admin.account import (
	AccountCreationForm, 
	AccountChangeForm,
)
from ecomm.apps.account.models import (
	Account,
	Profile,
)


class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	verbose_name_plural = _('Profile')
	fk_name = 'account'

@admin.register(Account)
class AccountAdmin(UserAdmin):
	add_form = AccountCreationForm
	form = AccountChangeForm
	model = Account
	list_display = [
		'email', 
		'username',
	]
	list_select_related = [
		'profile', 
	]
	inlines = [
		ProfileInline, 
	]
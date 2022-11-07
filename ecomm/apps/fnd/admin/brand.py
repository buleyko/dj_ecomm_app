from django import forms
from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from ecomm.vendors.base.model import AdminBaseModel
from ecomm.apps.fnd.models import Brand
from ecomm.vendors.mixins.model import ExcludeTimestampsMixin


@admin.register(Brand)
class BrandAdmin(AdminBaseModel, ExcludeTimestampsMixin):

	fieldsets = (
		(None, {
			'fields': (
				('is_shown', 'is_blocked',), 
				'slug',
				'name',
				'created_by',
				'fnd', 
			)
		}),
	)
	list_display = [
		'slug', 
		'get_name',
		'is_shown', 
		'blocked',
	]
	list_editable = [
		'is_shown',
	]
	list_filter = [
		'slug',
	]

	def blocked(self, instance):
		return instance.is_blocked == True
	blocked.boolean = True
	blocked.short_description = _('Blocked')


	def get_name(self, instance):
		return instance.get_name_by(get_language())
	get_name.short_description = _('Name')
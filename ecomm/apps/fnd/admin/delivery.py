import copy
from django import forms
from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from ecomm.vendors.base.model import AdminBaseModel
from ecomm.apps.fnd.models import Delivery
from ecomm.vendors.mixins.model import ExcludeTimestampsMixin


@admin.register(Delivery)
class DeliveryAdmin(AdminBaseModel, ExcludeTimestampsMixin):
		
	fieldsets = (
		(None, {
			'fields': (
				('is_shown', 'is_blocked',), 
				'name',
				'price',
				'method',
				'time_frame',
				'time_window',
				'position', 
				'fnd',
			)
		}),
	)
	list_display = [
		'get_name', 
		'price',
		'method',
	]

	def get_name(self, instance):
		return instance.get_name_by(get_language())
	get_name.short_description = _('Name')
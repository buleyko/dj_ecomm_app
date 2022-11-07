import copy
from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from ecomm.vendors.mixins.model import ExcludeTimestampsMixin
from ecomm.apps.fnd.models import (
	Fnd,
	FndTranslation,
)


class FndTranslationInline(admin.StackedInline):
	model = FndTranslation
	extra = 1
	fieldsets = [
		('Translation', { 'fields': [
			('lang',), 
			('description',),
		]
		}),
		('SEO', {
			'fields': (
				('meta_keywords', 'meta_description',)
			)
		})
	]

@admin.register(Fnd)
class FndAdmin(AdminBaseModel, ExcludeTimestampsMixin):

	fieldsets = (
		(None, {
			'fields': (
				('is_shown', 'is_blocked',), 
				'slug', 
				'name',
				'main_layout', 
				'content_layout', 
				'theme', 
				'logo',
			)
		}),
	)
	list_display = [
		'slug', 
		'get_name',
	]
	list_filter = [
		'slug',
	]
	inlines = [
		FndTranslationInline,
	]

	def get_name(self, instance):
		return instance.get_name_by(get_language())
	get_name.short_description = _('Name')

	
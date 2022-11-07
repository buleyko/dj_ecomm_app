import copy
from django import forms
from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from ecomm.apps.fnd.models import (
	SaleType,
	Coupon,
	Sale,
	SaleTranslation,
)
from ecomm.vendors.mixins.model import ExcludeTimestampsMixin



@admin.register(SaleType)
class SaleTypeAdmin(AdminBaseModel, ExcludeTimestampsMixin):
	pass


@admin.register(Coupon)
class CouponAdmin(AdminBaseModel):
	fieldsets = (
		(None, {
			'fields': (
				('is_shown', 'is_blocked',), 
				'slug',
				'name',
				'coupon_code',
				'created_by',
				'fnd',
			)
		}),
	)
	list_display = [
		'slug', 
		'coupon_code',
	]


class SaleTranslationInline(admin.StackedInline):
	model = SaleTranslation
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


@admin.register(Sale)
class SaleAdmin(AdminBaseModel, ExcludeTimestampsMixin):
	inlines = [
		SaleTranslationInline,
	]
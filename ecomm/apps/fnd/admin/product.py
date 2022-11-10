import copy
from django.contrib import admin
from django.conf import settings
from ecomm.vendors.base.model import AdminBaseModel
from ecomm.vendors.mixins.model import ExcludeTimestampsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from ecomm.apps.fnd.models import (
	ProductBase,
	ProductBaseTranslation,
	Product,
	ProductAttribute,
	ProductAttributeValue,
	ProductType,
	Media,
)
from ecomm.vendors.mixins.model import ExcludeTimestampsMixin



class ProductBaseTranslationInline(admin.StackedInline):
	model = ProductBaseTranslation
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

@admin.register(ProductBase)
class ProductBaseAdmin(AdminBaseModel, ExcludeTimestampsMixin):
	fieldsets = (
		(None, {
			'fields': (
				('is_shown', 'is_blocked',), 
				'slug',
				'name',
				'created_by',
				'category',
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
	inlines = [
		ProductBaseTranslationInline,
	]
	def blocked(self, instance):
		return instance.is_blocked == True
	blocked.boolean = True
	blocked.short_description = _('Blocked')


	def get_name(self, instance):
		return instance.get_name_by(get_language())
	get_name.short_description = _('Name')


class MediaInline(admin.StackedInline):
	model = Media
	extra = 1
	fieldsets = (
		(None, {
			'fields': (
				('product', ),
				'img',
				'alt_text',
				'is_feature',
				'fnd',
			)
		}),
	)


class ProductAttributeValuesInline(admin.StackedInline):
	model = Product.attribute_values.through
	extra = 1
	fieldsets = (
		(None, {
			'fields': (
				('attribute_values'),
			)
		}),
	)

@admin.register(Product)
class ProductAdmin(AdminBaseModel, ExcludeTimestampsMixin):

	def get_queryset(self, request):
		qs = super(ProductAdmin, self).get_queryset(request)
		return qs.select_related('prod_base')

	fieldsets = (
		(None, {
			'fields': (
				('is_shown', 'is_blocked',), 
				'slug',
				'sku',
				'thumb',
				'ext_name',
				'created_by',
				'fnd', 
				'prod_base',
				'brand',
				'product_type',
				'price',
				'sale_price',
				'is_default',
				'is_digital',
			)
		}),
	)
	list_display = [
		'slug', 
		'get_name',
		'price',
		'is_shown',
		'blocked'
	]
	list_editable = [
		'is_shown',
	]
	list_filter = [
		'slug',
	]
	inlines = [
		ProductAttributeValuesInline,
		MediaInline,
	]

	def blocked(self, instance):
		return instance.is_blocked == True
	blocked.boolean = True
	blocked.short_description = _('Blocked')

	def get_name(self, instance):
		return f'{instance.prod_base.get_name_by(get_language())}({instance.name_ext()})'
	get_name.short_description = _('Name')

	# def save_model(self, request, obj, form, change):
	# 	# obj.user = request.user
	# 	super().save_model(request, obj, form, change)



@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
	pass


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
	list_display = [
		'product_attribute',
		'value',
	]

class ProductTypeAttributeInline(admin.StackedInline):
	model = ProductType.product_type_attributes.through
	extra = 1
	fieldsets = [
		(None, 
			{ 'fields': ['prod_attribute']
		}),
	]


@admin.register(ProductType)
class ProductTypeAdmin(AdminBaseModel):
	fieldsets = (
		(None, {
			'fields': (
				('is_shown', 'is_blocked',), 
				'slug',
				'name',
				'category',
				'fnd',
			)
		}),
	)
	list_display = [
		'slug',
		'get_name', 
	]
	inlines = [
		ProductTypeAttributeInline,
	]

	def get_name(self, instance):
		return instance.get_name_by(get_language())
	get_name.short_description = _('Name')


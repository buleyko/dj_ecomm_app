from django.contrib import admin
from ecomm.vendors.base.model import AdminBaseModel
from ecomm.vendors.mixins.model import ExcludeTimestampsMixin
from ecomm.apps.fnd.models import (
	Order,
	OrderProduct,
)


@admin.register(Order)
class OrderAdmin(AdminBaseModel, ExcludeTimestampsMixin):
	fieldsets = (
		(None, {
			'fields': (
				('is_shown', 'is_blocked',), 
				'account',
				'address',
				'total_paid',
				'order_key',
				'billing_status', 
				'created_by',
				'fnd',
			)
		}),
	)
	list_display = [
		'order_key', 
	]

@admin.register(OrderProduct)
class OrderProductAdmin(AdminBaseModel):
	fieldsets = (
		(None, {
			'fields': (
				('is_shown', 'is_blocked',), 
				'order',
				'product',
				'price',
				'quantity',
				'fnd',
			)
		}),
	)
	exclude = (
		'created_at', 
		'updated_at', 
		'deleted_at',
	)
	list_display = [
		'order', 
		'product',
		'price',
		'quantity',
	]

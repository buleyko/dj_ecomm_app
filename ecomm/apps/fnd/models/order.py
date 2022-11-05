from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.base.model import BaseModel
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
)
from django.contrib.auth import get_user_model
Account = get_user_model()



class Order(BaseModel, TimestampsMixin, SoftdeleteMixin):
	account = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='order_account',
		null=True, 
		blank=True,
	)
	email = models.EmailField(
		max_length=254, blank=True
	)
	address = models.CharField(
		max_length=250
	)
	city = models.CharField(
		max_length=100
	)
	phone = models.CharField(
		max_length=100
	)
	postal_code = models.CharField(
		max_length=20
	)
	country_code = models.CharField(
		max_length=4, 
		blank=True
	)
	total_paid = models.DecimalField(
		max_digits=5, 
		decimal_places=2
	)
	order_key = models.CharField(
		max_length=200
	)
	billing_status = models.BooleanField(
		default=False
	)
	payment = models.CharField( # 'paypal'
		max_length=200, 
		blank=True,
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='fnd_orders',
	)

	class Meta:
		verbose_name = _('Order')
		verbose_name_plural = _('Orders')
		ordering = ('-created_at',)

	def __str__(self):
		return str(self.order_key)

	list_values = [
		'order_key', 
		'total_paid',  
		'address__full_name', 
		'created_at'
	]


class OrderProduct(BaseModel):
	order = models.ForeignKey(
		Order, 
		related_name='order_orderproducts', 
		on_delete=models.CASCADE
	)
	product = models.ForeignKey(
		'Product', 
		related_name='prod_orderproducts', 
		on_delete=models.CASCADE
	)
	price = models.DecimalField(
		max_digits=5, 
		decimal_places=2
	)
	quantity = models.PositiveIntegerField(
		default=1
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='fnd_order_products',
	)

	def __str__(self):
		return str(self.id)
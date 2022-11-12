from django.db import models
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.base.model import BaseModel
from django.contrib.auth import get_user_model
Account = get_user_model()


class Address(BaseModel):
	full_name = models.CharField(
		_('Full Name'), 
		max_length=150
	)
	phone = models.CharField(
		_('Phone Number'), 
		max_length=50,
		null=True,
		blank=True
	)
	postcode = models.CharField(
		_('Postcode'), 
		max_length=50
	)
	address_line = models.CharField(
		_('Address Line'), 
		max_length=255
	)
	town_city = models.CharField(
		_('Town/City/State'), 
		max_length=150
	)
	delivery_instructions = models.CharField(
		_('Delivery Instructions'), 
		max_length=255
	)
	default = models.BooleanField(
		_('Default'), 
		default=False
	)
	account = models.ForeignKey(
		Account, 
		verbose_name=_('Account'), 
		on_delete=models.CASCADE
	)

	class Meta:
		verbose_name = _('Address')
		verbose_name_plural = _('Addresses')

	def __str__(self):
		return '{} Address'.format(self.full_name)
from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.base.model import BaseModel
from ecomm.vendors.mixins.model import NameByLangMixin
from django.contrib.auth import get_user_model
Account = get_user_model()



class Delivery(BaseModel, NameByLangMixin):
	IS = 'IS' 
	HD = 'HD'
	DD = 'DD'
	DELIVERY_CHOICES = [
		(IS, _('In Store')),
		(HD, _('Home Delivery')),
		(DD, _('Digital Delivery')),
	]
	name = models.JSONField(
		help_text=_('Required'),
	)
	price = models.DecimalField(
		verbose_name=_('delivery price'),
		help_text=_('Maximum 999.99'),
		error_messages={
			'name': {
				'max_length': _('The price must be between 0 and 999.99.'),
			},
		},
		max_digits=5,
		decimal_places=2,
	)
	method = models.CharField(
		choices=DELIVERY_CHOICES,
		verbose_name=_('delivery_method'),
		help_text=_('Required'),
		max_length=255,
	)
	time_frame = models.CharField( # 2-3 days
		verbose_name=_('delivery timeframe'),
		help_text=_('Required'),
		max_length=255,
		null = True,
		blank = True,
	)
	time_window = models.CharField( # 13-14 p.m
		verbose_name=_("delivery window"),
		help_text=_("Required"),
		max_length=255,
		null = True,
		blank = True,
	)
	position = models.IntegerField(
		verbose_name=_('list order'), 
		help_text=_('Required'), 
		default=0
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='fnd_delivery',
	)

	class Meta:
		verbose_name = _('Delivery')
		verbose_name_plural = _('Deliveries')
		ordering = ['position']

	def __str__(self):
		return self.get_name_by(get_language())

	list_values = [
		'id',
		'title',
		'translation__name',
		'price',
		
	]
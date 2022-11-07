from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.base.model import BaseModel
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
	NameByLangMixin,
)
from django.contrib.auth import get_user_model
Account = get_user_model()

def brand_logo_upload_to(instance, filename):
    return f'fnd/{instance.fnd_id}/brand/{instance.slug}/{filename}'


class Brand(BaseModel, TimestampsMixin, SoftdeleteMixin, NameByLangMixin):
	slug = models.SlugField(
		max_length=180,
		unique=True,
		verbose_name=_('Brand URL'),
	)
	name = models.JSONField(
		max_length=120, 
	)
	site = models.CharField(
		max_length=180,
		null = True,
		blank = True,
	)
	logo = models.ImageField(
		upload_to=brand_logo_upload_to, 
		null=True, 
		blank=True
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='brand_creator',
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='brand_updater', 
		null=True,
		blank=True,
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='brands',
	)

	class Meta:
		verbose_name = _('Brand')
		verbose_name_plural = _('Brands')

	def __str__(self):
		return self.slug
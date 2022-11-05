from django.db import models
from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from mptt.models import (
	MPTTModel, 
	TreeForeignKey, 
	TreeManyToManyField,
)
from ecomm.vendors.base.model import BaseModel
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
)
from django.contrib.auth import get_user_model
Account = get_user_model()

def cat_thumb_upload_to(instance, filename):
    return f'fnd/{instance.fnd_id}/category/thumb/{instance.slug}/{filename}'



class Category(MPTTModel, BaseModel, TimestampsMixin, SoftdeleteMixin):
	slug = models.SlugField(
		max_length=150,
		unique=True,
		verbose_name=_('Category URL'),
		help_text=_(
			'format: required, letters, numbers, underscore, or hyphens'
		),
	)
	name = models.JSONField(
		max_length=180, 
	)
	thumb = models.ImageField(
		upload_to=cat_thumb_upload_to, 
		null=True, 
		blank=True
	)
	parent = TreeForeignKey(
		'self',
		null=True,
		blank=True,
		on_delete=models.PROTECT,
		related_name='children',
		verbose_name=_('parent of category'),
		help_text=_('format: not required'),
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='category_creator',
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='category_updater', 
		null=True,
		blank=True,
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='categories',
	)

	class MPTTMeta:
		order_insertion_by = ['created_at']

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')

	def __str__(self):
		return self.slug

	def thumbUrl(self):
		try:
			url = self.thumb.url
		except:
			url = static(settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return url
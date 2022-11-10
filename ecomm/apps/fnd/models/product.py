from django.db import models
from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from ecomm.vendors.helpers.image import resize_image
from ecomm.vendors.base.model import BaseModel
from django.core.validators import (
	MinValueValidator,
	MaxValueValidator,
)
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
	MetaDataMixin,
	NameByLangMixin,
)
from django.db.models import F
from django.contrib.auth import get_user_model
Account = get_user_model()



class ProductAttribute(BaseModel, NameByLangMixin):
	slug = models.SlugField(
		max_length=255,
		unique=True,
	)
	name = models.JSONField(
		null=True, 
		blank=True
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='prod_attributes',
	)

	def __str__(self):
		return self.slug

	class Meta:
		verbose_name = _('Product attribute')
		verbose_name_plural = _('Product attributes')


class ProductAttributeValue(BaseModel):
	product_attribute = models.ForeignKey(
		ProductAttribute,
		related_name='values',
		on_delete=models.PROTECT,
	)
	value = models.CharField(
		max_length=255,
	)
	trs = models.JSONField(
		null=True, 
		blank=True
	)
	def trs_val(self):
		try:
			return self.trs[get_language()]
		except:
			return self.value

	def __str__(self):
		return f'{self.product_attribute} ({self.value})'


class ProductType(BaseModel, NameByLangMixin):
	slug = models.SlugField(
		max_length=255,
		unique=True,
	)
	name = models.JSONField()
	category = models.ForeignKey(
		'Category',
		related_name='types',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
	)
	product_type_attributes = models.ManyToManyField(
		ProductAttribute,
		related_name='types',
		through='ProductTypeAttribute',
	)
	in_menu = models.BooleanField(
		default = False,
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='prod_types',
	)

	def __str__(self):
		return self.slug

	class Meta:
		verbose_name = _('Product type')
		verbose_name_plural = _('Product types')



class ProductTypeAttribute(BaseModel):
	prod_attribute = models.ForeignKey(
		ProductAttribute,
		related_name='attribute',
		on_delete=models.PROTECT,
	)
	prod_type = models.ForeignKey(
		ProductType,
		related_name='type',
		on_delete=models.PROTECT,
	)

class ProductAttributeValues(BaseModel):
	attribute_values = models.ForeignKey(
		ProductAttributeValue,
		related_name='values',
		on_delete=models.PROTECT,
	)
	product = models.ForeignKey(
		'Product',
		related_name='attr_values',
		on_delete=models.PROTECT,
	)

	class Meta:
		unique_together = (('attribute_values', 'product'),)



class ProductBase(BaseModel, TimestampsMixin, SoftdeleteMixin, NameByLangMixin):
	slug = models.SlugField(
		max_length=180,
		unique=True,
		verbose_name=_('Product(base) URL'),
	)
	name = models.JSONField()
	short_desc = models.JSONField(
		null=True, 
		blank=True
	)
	category = models.ForeignKey(
		'Category',
		related_name='base_prods',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='prod_base_creator',
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='prod_base_updater', 
		null=True,
		blank=True,
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='base_prods',
	)

	class Meta:
		verbose_name = _('Base product')
		verbose_name_plural = _('Base products')

	def __str__(self):
		return self.slug

	defer_values = [
		'created_by',
		'updated_by',
		'fnd', 
	]


class ProductBaseTranslation(MetaDataMixin):
	lang = models.CharField(
		max_length=5, 
		default = settings.LANGUAGE_CODE,
	)
	description = models.TextField(
		null=True, 
		blank=True
	)
	prod_base = models.ForeignKey(
		ProductBase, 
		related_name='translation', 
		on_delete=models.CASCADE
	)

	class Meta:
		verbose_name = _('Base product translation')
		verbose_name_plural = _('Base product translations')



def prod_thumb_upload_to(instance, filename):
	return f'fnd/{instance.fnd_id}/prod/{instance.slug}/thumb/{filename}'


class Product(BaseModel, TimestampsMixin, SoftdeleteMixin):
	slug = models.SlugField(
		max_length=255,
		unique=True,
		verbose_name=_('Product URL'),
	)
	sku = models.CharField(
		max_length=20,
		unique=True,
	)
	thumb = models.ImageField(
		upload_to=prod_thumb_upload_to, 
		null=True, 
		blank=True
	)
	# extension for name - red,small etc. ({'en':['red', 'small']}) 
	ext_name = models.JSONField( 
		default = dict
	)
	full_name = models.CharField(
		max_length=500,
	)
	prod_base = models.ForeignKey(
		ProductBase, 
		related_name='base_prods', 
		on_delete=models.CASCADE
	)
	brand = models.ForeignKey(
		'Brand',
		related_name='prod',
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
	)
	product_type = models.ForeignKey(
		ProductType, 
		related_name='prod', 
		on_delete=models.PROTECT
	)
	attribute_values = models.ManyToManyField(
		'ProductAttributeValue',
		related_name='prods',
		through='ProductAttributeValues',
	)
	is_default = models.BooleanField(
		default=False,
	)
	price = models.DecimalField(
		max_digits=5,
		decimal_places=2,
		validators=[
			MinValueValidator(settings.MIN_PRICE),
			MaxValueValidator(settings.MAX_PRICE),
		]
	)
	sale_price = models.DecimalField(
		max_digits=5,
		decimal_places=2,
		blank=True,
		null=True,
		validators=[
			MinValueValidator(settings.MIN_PRICE),
			MaxValueValidator(settings.MAX_PRICE),
		],
	)
	is_digital = models.BooleanField(
		default=False,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='prod_creator',
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='prod_updater', 
		null=True,
		blank=True,
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='fnd_prods',
	)

	class Meta:
		verbose_name = _('Product')
		verbose_name_plural = _('Products')
		ordering = ('-created_at',)

	def thumbUrl(self):
		try:
			url = self.thumb.url
		except:
			url = static(settings.DEFAULT_IMAGE['PLACEHOLDER'])
		return url

	def name_ext(self):
		try:
			return self.ext_name[get_language()]
		except:
			return ''

	def save(self, *args, **kwargs):
		_full_name = [*self.prod_base.name.values(), *self.ext_name.values()]
		self.full_name = '@'.join(_full_name)
		super().save(*args, **kwargs)
		if self.thumb:
			thumb_img = resize_image(self.thumb.path, settings.THUMB_WIDTH)
			if thumb_img:
				thumb_img.save(self.thumb.path)

	list_values = [
		'id', 
		'prod_base_id', 
		'prod_base__name', 
		'thumb', 
		'ext_name', 
		'price', 
		'sale_price',
	]

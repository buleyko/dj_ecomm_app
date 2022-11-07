from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
	MinValueValidator,
	MaxValueValidator,
)
from ecomm.vendors.base.model import BaseModel
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
	MetaDataMixin,
	NameByLangMixin,
)
from decimal import Decimal
from django.contrib.auth import get_user_model
Account = get_user_model()



class SaleType(BaseModel, NameByLangMixin):
	slug = models.SlugField(
		max_length=80, 
		unique=True
	)
	name = models.JSONField(
		max_length=500,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='sale_type_creator',
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='sale_type_updater', 
		null=True,
		blank=True,
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='fnd_sale_types',
	)

	def __str__(self):
		return self.slug

	class Meta:
		verbose_name = _('Sale type')
		verbose_name_plural = _('Sale types')


class Coupon(BaseModel, NameByLangMixin):
	slug = models.SlugField(
		max_length=255, 
		unique=True
	)
	name = models.JSONField(
		max_length=500,
	)
	coupon_code = models.CharField(
		max_length=20,
		unique = True,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='coupon_creator',
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='coupon_updater', 
		null=True,
		blank=True,
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='fnd_coupons',
	)

	def __str__(self):
		return self.slug

	class Meta:
		verbose_name = _('Coupon')
		verbose_name_plural = _('Coupons')



class Sale(BaseModel, TimestampsMixin, SoftdeleteMixin):
	slug = models.SlugField(
		max_length=255, 
		unique=True
	)
	sale_reduction = models.IntegerField(
		default=0
	)
	is_schedule = models.BooleanField(
		default=False
	)
	sale_start = models.DateField()
	sale_end = models.DateField()

	sale_type = models.ForeignKey(
		SaleType,
		related_name='sale_types',
		on_delete=models.PROTECT,
	)

	coupon = models.ForeignKey(
		Coupon,
		related_name='sale_coupons',
		on_delete=models.PROTECT,
		null=True,
		blank=True,
	)

	prod_sale = models.ManyToManyField(
		'Product',
		related_name='prod_sales',
		through='ProductSale',
	)

	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='sale_creator',
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='sale_updater', 
		null=True,
		blank=True,
	)
	fnd = models.ForeignKey(
		'Fnd',
		on_delete=models.CASCADE, 
		related_name='store_sales',
	)

	def clean(self):
		if self.sale_start > self.sale_end:
			raise ValidationError(_('End data before the start date'))

	def __str__(self):
		return self.slug


class SaleTranslation(MetaDataMixin):
	lang = models.CharField(
		max_length=5, 
		default = settings.LANGUAGE_CODE,
	)
	description = models.TextField(
		null=True, 
		blank=True,
	)
	sale = models.ForeignKey(
		Sale, 
		related_name='translation', 
		on_delete=models.CASCADE
	)

	class Meta:
		verbose_name = _('Sale translation')
		verbose_name_plural = _('Sale translations')


class ProductSale(models.Model):
	product_id = models.ForeignKey(
		'Product',
		related_name='prods_sales',
		on_delete=models.PROTECT,
	)
	sale_id = models.ForeignKey(
		Sale,
		related_name='sale',
		on_delete=models.CASCADE,
	)
	sale_price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		default=Decimal('0.00'),
		validators=[
			MinValueValidator(Decimal('0.00')),
		],
	)
	price_override = models.BooleanField(
		default=False,
	)

	class Meta:
		unique_together = (('product_id', 'sale_id'),)


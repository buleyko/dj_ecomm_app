from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.base.model import BaseModel



class Stock(BaseModel):
    product = models.OneToOneField(
        'Product',
        related_name='stock_prod',
        on_delete=models.PROTECT,
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
    )
    units = models.IntegerField(
        default=0,
    )
    units_sold = models.IntegerField(
        default=0,
    )
    fnd = models.ForeignKey(
        'Fnd',
        on_delete=models.CASCADE, 
        related_name='store_stock',
    )

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
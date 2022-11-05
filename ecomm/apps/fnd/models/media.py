from django.db import models
from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.helpers.image import resize_image
from ecomm.vendors.base.model import BaseModel
from .product import Product
from django.contrib.auth import get_user_model
Account = get_user_model()

def product_media_upload_to(instance, filename):
    return f'fnd/{instance.fnd_id}/prod/{instance.product.slug}/media/{filename}'


class Media(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="media",
    )
    img = models.ImageField(
        upload_to=product_media_upload_to
    )
    alt_text = models.JSONField(
        max_length=80, 
		null=True, 
		blank=True,
	)
    is_feature = models.BooleanField(
        default=False,
    )
    fnd = models.ForeignKey(
        'Fnd',
        on_delete=models.CASCADE, 
        related_name='fnd_media',
    )

    class Meta:
        verbose_name = _('Product image')
        verbose_name_plural = _('Product images')

    def imgUrl(self):
        try:
            url = self.img.url
        except:
            url = static(settings.DEFAULT_IMAGE['PLACEHOLDER'])
        return url

    def alt(self):
        try:
            return self.alt_text[get_language()]
        except:
            return ''

    def save(self, size=settings.IMAGE_WIDTH, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.img:
            media_img = resize_image(self.img.path, size)
            if media_img:
                media_img.save(self.img.path)
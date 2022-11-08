from django.db import models
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from ecomm.vendors.base.model import BaseModel
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
)

class Account(AbstractUser, BaseModel, TimestampsMixin, SoftdeleteMixin):
    fnds = models.JSONField(
        null=True, 
        blank=True
    )
    wish = models.JSONField(
        null=True, 
        blank=True,
    )
    comparison = models.JSONField(
        null=True, 
        blank=True,
    )
    
    class Meta:
        verbose_name =  _('Account')
        verbose_name_plural =  _('Accounts')

    def __str__(self):
        return self.username

    @classmethod
    def get_by_uid(cls, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64)) 
            user = cls.objs.get(pk=uid)
        except(TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None
        return user


    def get_wish(self, alias=settings.FND_ALIAS):
        try:
            return self.wish[alias]
        except:
            return []

    def get_comparison(self, alias=settings.FND_ALIAS):
        try:
            return self.comparison[alias]
        except:
            return []

    def update_wish(self, prod_id, key='add', alias=settings.FND_ALIAS):
        if key == 'add':
            if self.wish:
                self.wish.append(str(prod_id))
            else:
                self.wish = [str(prod_id)]
        elif key == 'remove':
            if self.wish:
                self.wish.remove(str(prod_id))
        self.save(update_fields=['wish'])

    def update_comparison(self, prod_id, key='add', alias=settings.FND_ALIAS):
        if key == 'add':
            if self.comparison:
                self.comparison.append(str(prod_id))
            else:
                self.comparison = [str(prod_id)]
        elif key == 'remove':
            if self.comparison:
                self.comparison.remove(str(prod_id))
        self.save(update_fields=['comparison'])


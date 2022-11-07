import logging
from django.db import models
from django.contrib import admin
from django.db.models import Q
from django.conf import settings

logger = logging.getLogger("main")


class BaseQuerySet(models.QuerySet):
	""" Querysets for main tables """
	def blocked(self, blocked=True):
		return self.filter(is_blocked=blocked)

	def shown(self, shown=True):
		return self.filter(is_shown=shown)

	def active(self, active=True):
		return self.filter(is_active=active)

	def valid(self, blocked=False, shown=True):
		""" filter blocked:false, shown:true """
		return self.filter(Q(is_blocked=blocked), Q(is_shown=shown))

	def fnd(self, alias=settings.FND_ALIAS):
		return self.filter(fnd_id=alias)

	def by_raw(self, query_str, params):
		return self.raw(query_str, params)


class BaseManager(models.Manager):
	""" Manager for main tables """
	def get_queryset(self):
		return BaseQuerySet(self.model, using=self._db)

	def blocked(self, blocked=True):
		return self.get_queryset().blocked(blocked)

	def shown(self, shown=True):
		return self.get_queryset().shown(shown)

	def active(self, active=True):
		return self.get_queryset().active(active)

	def valid(self, blocked=False, shown=True):
		return self.get_queryset().valid(blocked, shown)

	def fnd(self, alias=settings.FND_ALIAS):
		return self.get_queryset().fnd(alias)

	def by_raw(self, query_str, params):
		return self.get_queryset().by_raw(query_str, params)


class BaseModel(models.Model):
	""" Base model for main tables (abstract) """
	is_blocked = models.BooleanField(
		default=False
	)   # block for all actions
	is_shown = models.BooleanField(
		default=False
	) # show or hidden

	objs = BaseManager()
	
	class Meta:
		abstract = True

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		super().delete(*args, **kwargs)


class AdminBaseModel(admin.ModelAdmin):
    empty_value_display = settings.EMPTY_VALUE

    exclude = (
		'created_at', 
		'updated_at', 
		'deleted_at',
	)

	
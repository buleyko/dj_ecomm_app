import logging
from django.db import models
from django.contrib import admin
from django.db.models import Prefetch
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

	def filter_in_if_args_exists(self, key, arguments=[]):
		if arguments:
			filter_dict = {key: arguments}
			return self.filter(**filter_dict)
		else:
			return self

	def filter_contains_if_args_exists(self, key, arguments=[]):
		if arguments:
			_q = Q()
			conn = Q.OR
			for arg in arguments:
				search_dict = {key: arg}
				_q.add(Q(**search_dict), conn)
			return self.filter(_q)
		else:
			return self

	def filter_contains_if_arg_exist(self, keys, argument=''):
		''' like this
		[
            'prod_base__title__contains', 
            ('prod_base__translation__name__contains', 'or',)
        ], argument
		'''
		if argument:
			if isinstance(keys, list):
				_q = Q()
				for key in keys:
					if isinstance(key, tuple):
						conn = Q.AND if key[1]!='or' else Q.OR
						_q.add(Q(**{key[0]: argument}), conn)
					else:
						_q.add(Q(**{key: argument}), Q.AND)
			else:
				_q = Q(**{keys: argument})
			return self.filter(_q)
		else:
			return self

	def translation_by(self, lang=settings.LANGUAGE_CODE):
		return self.filter(translation__lang = lang)
	
	def prefetch_translation_by(self, model_translation, lang=settings.LANGUAGE_CODE, defers=[]):
		return self.prefetch_related(
			Prefetch('translation', 
				queryset=model_translation.objs.filter(lang_id=lang).defer(*defers), 
				to_attr='tr'
			)
		)

	def prefetch_translation(self, model_translation, defers=[]):
		return self.prefetch_related(
			Prefetch('translation', 
				queryset=model_translation.objs.all().defer(*defers), 
				to_attr='tr'
			)
		)

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

	def filter_in_if_args_exists(self, key, arguments=[]):
		return self.get_queryset().filter_in_if_args_exists(key, arguments)

	def filter_contains_if_args_exists(self, key, arguments=[]):
		return self.get_queryset().filter_contains_if_arg_exists(key, arguments)

	def filter_contains_if_arg_exist(self, keys, arguments=''):
		return self.get_queryset().filter_contains_if_arg_exist(keys, argument)

	def translation_by(self, lang=settings.LANGUAGE_CODE):
		return self.get_queryset().translation_by(lang)

	def prefetch_translation_by(self, model_translation, lang=settings.LANGUAGE_CODE, defers=[]):
		return self.get_queryset().prefetch_translation_by(model_translation, lang=lang, defers=defers)

	def prefetch_translation(self, model_translation, defers=[]):
		return self.get_queryset().prefetch_translation(self, model_translation, defers=defers)

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


	
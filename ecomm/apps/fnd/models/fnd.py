from django.db import models
from django.conf import settings
from django.templatetags.static import static
from django.dispatch import receiver
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from ecomm.vendors.base.model import BaseModel
from ecomm.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
	MetaDataMixin,
)
from django.contrib.auth import get_user_model
Account = get_user_model()


def fnd_logo_upload_to(instance, filename):
    return f'fnd/{instance.alias}/logo/{filename}'

class Fnd(BaseModel, TimestampsMixin, SoftdeleteMixin):
	UPPER = 'layouts/upper.html'
	LOWER = 'layouts/lower.html'
	LEFT  = 'layouts/left.html'
	RIGHT = 'layouts/right.html'
	COL = 'list_container-col'
	ROW = 'list_container-row'
	LIGHT = 'light'
	DARK = 'dark'

	MAIN_LAYOUT = [
		(UPPER,  _('Upper')),
		(LOWER,  _('Lower')),
		(LEFT,   _('Left')),
		(RIGHT,  _('Right')),
	]
	CONTENT_LAYOUT = [
		(ROW, _('Row')),
		(COL, _('Column')),
	]
	THEME = [
		(LIGHT, _('Light')),
		(DARK,  _('Dark')),
	]

	alias = models.CharField(
		max_length=30, 
		primary_key=True
	)
	name = models.JSONField(
		max_length=80, 
		null=True, 
		blank=True,
	)
	logo = models.ImageField(
		upload_to=fnd_logo_upload_to, 
		null=True, 
		blank=True
	)
	main_layout = models.CharField(
		max_length=20, 
		choices=MAIN_LAYOUT, 
		default=UPPER
	)
	content_layout = models.CharField(
		max_length=20, 
		choices=CONTENT_LAYOUT, 
		default=ROW
	)
	theme = models.CharField(
		max_length=6, 
		choices=THEME, 
		default=LIGHT
	)
	langs = models.JSONField(
		null=True, 
		blank=True
	)

	class Meta:
		verbose_name = _('Foundation')
		verbose_name_plural = _('Foundations')

	def __str__(self):
		return self.alias

	def logoUrl(self):
		try:
			url = self.logo.url
		except:
			url = static(settings.DEFAULT_IMAGE)
		return url

	# def set_langs(self):
	# 	# ...
	# 	self.save(update_fields=['langs'])

	def set_options(self, session):
		options = {
			'theme': self.theme,
			'content_layout': self.content_layout,
		}
		if session.get('options', False):
			user_options = session['options']

			if user_options.get('theme', False):
				options['theme'] = user_options['theme']

			if user_options.get('content_layout', False):
				options['content_layout'] = user_options['content_layout']

		return options

	context_values = [
		'alias',
		'name',
		'main_layout', 
		'content_layout',
		'theme', 
		'langs',
	]

class FndTranslation(MetaDataMixin):
	lang = models.CharField(
		max_length=5, 
		default = settings.LANGUAGE_CODE,
	)
	description = models.TextField(
		null=True, 
		blank=True,
	)
	fnd = models.ForeignKey(
		Fnd, 
		related_name='translation', 
		on_delete=models.CASCADE,
	)

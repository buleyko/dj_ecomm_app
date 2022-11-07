from django.db import models
from django.utils.timezone import now


class SoftdeleteMixin(models.Model):
	""" Soft delete date time (abstract) """
	deleted_at = models.DateTimeField(
		null=True, 
		blank=True
	)

	class Meta:
		abstract = True


class TimestampsMixin(models.Model):
	""" Date time for created and updated (abstract) """
	created_at = models.DateTimeField(
		default = now,
		editable=False
	)
	updated_at = models.DateTimeField(
		null=True, 
		blank=True
	)

	class Meta:
		abstract = True


class MetaDataMixin(models.Model):
	""" String data for SEO: keywords and description (abstract) """
	meta_keywords = models.CharField(
		max_length=255,
		null=True, 
		blank=True
	)
	meta_description = models.CharField(
		max_length=255, 
		null=True, 
		blank=True
	)
	# meta_author = models.CharField(
	# 	max_length=255, 
	# 	null=True, 
	# 	default='',
	# )
	
	class Meta:
		abstract = True


class NameByLangMixin:
	def get_name_by(self, lang):
		name = self.name.get(lang, False)
		if not name:
			name = self.name.get('title', None)
		return name



class ExcludeTimestampsMixin:
	exclude = (
		'created_at', 
		'updated_at', 
		'deleted_at',
	)
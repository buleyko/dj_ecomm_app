from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
Account = get_user_model()

def profile_photo_upload_to(instance, filename):
	return f'account/{instance.id}/photo/{filename}'

class Profile(models.Model):
	MALE = 'male'
	FEMALE = 'female'

	SEX_CHOICES = [
		(MALE,   _('Male')),
		(FEMALE, _('Female')),
	]

	account = models.OneToOneField(
		Account, 
		on_delete=models.CASCADE
	)
	photo = models.ImageField(
		upload_to=profile_photo_upload_to, 
		null=True, 
		blank=True
	)
	phone = models.CharField(
		max_length=25, 
		null=True, 
		blank=True
	)
	age = models.IntegerField(
		null=True, 
		blank=True
	)
	birthdate = models.DateField(
		null=True, 
		blank=True
	)
	sex = models.CharField(
		max_length=8, 
		choices=SEX_CHOICES, 
		default=MALE
	)

	class Meta:
		verbose_name = _('Profile')
		verbose_name_plural = _('Profiles')
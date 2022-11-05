import pytest
from django.conf import settings
from ecomm.apps.fnd.tests.factories import (
	LangFactory,
	FndFactory,
	FndTranslationFactory,
)


@pytest.fixture
def create_admin_user(django_user_model):
	return django_user_model.objects.create_superuser(
		'admin', 'admin@mail.com', 'password'
	)


@pytest.fixture
def create_test_fnd(db):
	fnd = FndFactory(alias=settings.FND_ALIAS)
	for code, _ in settings.LANGUAGES:
		fnd_translation = FndTranslationFactory(
			name='Fnd name', 
			fnd = fnd,
			lang = LangFactory(code=code),
		)
	return fnd

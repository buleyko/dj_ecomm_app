import pytest
from .factories import (
	LangFactory,
	FndFactory,
	FndTranslationFactory,
)

@pytest.mark.models
@pytest.mark.django_db
def test_language_create():
	language = LangFactory(
		code='en'
	)
	assert language.code == 'en'


@pytest.mark.models
@pytest.mark.django_db
def test_fnd_create():
	fnd = FndFactory(
		alias = 'fnd-one'
	)
	assert fnd.alias == 'fnd-one'


@pytest.mark.models
@pytest.mark.django_db
@pytest.mark.parametrize(
	'code', ['en', 'ru']
)
def test_fnd_translation_create(code):
	language = LangFactory(code=code)
	fnd = FndFactory()
	fnd_translation = FndTranslationFactory(
		name='Fnd name', 
		fnd = fnd,
		lang = language,
	)
	assert fnd_translation.name == 'Fnd name'
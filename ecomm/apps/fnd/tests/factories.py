import factory
from django.conf import settings
from faker import Faker
fake = Faker()

from ecomm.apps.fnd import models


class FndFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Fnd 

    alias = factory.Sequence(lambda n: f'fnd_{n}')
    name = {'en':'Foundation-EN', 'ru':'Foundation-RU'}
    langs = [
        {'code': 'en', 'title':'EN', 'is_default': True}, 
        {'lang': 'ru', 'title':'RU',  'is_default': False},
    ]
    is_shown = 'True'

class FndTranslationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FndTranslation

    description = fake.text()
    lang = settings.LANGUAGE_CODE
    fnd = factory.SubFactory(FndFactory)
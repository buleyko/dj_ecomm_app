import factory
from faker import Faker
fake = Faker()

from ecomm.apps.fnd import models


class FndFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Fnd 

    alias = factory.Sequence(lambda n: f'fnd_{n}')
    langs = [{'lang': 'en', 'is_default': True}, {'lang': 'ru', 'is_default': False}]
    is_shown = 'True'

class FndTranslationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FndTranslation

    name = fake.lexify(text='fnd_??????')
    description = fake.text()
    lang = factory.SubFactory(LangFactory)
    fnd = factory.SubFactory(FndFactory)
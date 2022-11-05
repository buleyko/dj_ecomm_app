import factory
from faker import Faker
fake = Faker()

from ecomm.apps.account import models



class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Account

    username = factory.Sequence(lambda n: f'user{n}')
    first_name = 'First name'
    last_name = 'Last name'
    email = factory.Sequence(lambda n: f'mail_{n}@mail.com')
    is_staff = 'True'
    is_active = 'True'
    is_blocked = 'False'
    is_shown = 'True'


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile 

    account = factory.SubFactory(AccountFactory)
    photo = '/media/photo.png'
    phone = '555-55-55-55'
    age = 99
    birthdate = '2021-09-04'
    sex = 'male'


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Address  

    account = factory.SubFactory(AccountFactory)
    phone = '555-22-22-22'
    postcode = '33333'
    address_line = 'Address line 1'
    town_city = 'Some town'
    delivery_instructions = 'Delivery instructions'
    default = 'True'
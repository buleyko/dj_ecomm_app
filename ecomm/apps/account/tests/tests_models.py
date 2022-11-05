import pytest
from .factories import (
	AccountFactory,
	ProfileFactory,
	AddressFactory,
)


@pytest.mark.models
@pytest.mark.django_db
def test_account_create():
	account = AccountFactory(
		username='Test Account'
	)
	assert account.username == 'Test Account'


@pytest.mark.models
@pytest.mark.django_db
def test_profile_create():
	profile = ProfileFactory(
		phone='555-55-55-55', 
	)
	assert profile.phone == '555-55-55-55'


@pytest.mark.models
@pytest.mark.django_db
def test_address_create():
	address = AddressFactory(
		full_name='Address full name', 
	)
	assert address.full_name == 'Address full name'
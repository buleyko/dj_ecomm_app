import pytest
from django.urls import reverse


@pytest.mark.views
@pytest.mark.django_db
def test_home_view(create_test_fnd, client):
	response = client.get(reverse('fnd:home')) 
	assert response.status_code == 200
	assert response.templates[0].name == 'apps/fnd/home.html'


@pytest.mark.views
@pytest.mark.django_db
def test_checkout_view(create_test_fnd, client):
	response = client.get(reverse('fnd:checkout')) 
	assert response.status_code == 200
	assert response.templates[0].name == 'apps/fnd/checkout.html'


@pytest.mark.views
@pytest.mark.django_db
def test_cart_view(create_test_fnd, client):
	response = client.get(reverse('fnd:cart')) 
	assert response.status_code == 200
	assert response.templates[0].name == 'apps/fnd/cart.html'
import pytest
from django.urls import reverse


@pytest.mark.views
@pytest.mark.django_db
def test_signin_view(create_test_fnd, client):
	response = client.get(reverse('account:signin')) 
	assert response.status_code == 200
	assert response.templates[0].name == 'apps/account/auth/login.html'


@pytest.mark.views
@pytest.mark.django_db
def test_signup_view(create_test_fnd, client):
	response = client.get(reverse('account:signup')) 
	assert response.status_code == 200
	assert response.templates[0].name == 'apps/account/auth/register.html'


@pytest.mark.views
@pytest.mark.django_db
def test_entry_view(create_test_fnd, create_admin_user, client):
	response = client.post(reverse('account:entry'), {
		'email': 'admin@mail.com', 
		'password': 'password', 
		'next_url': ''}
	) 
	assert response.status_code == 302

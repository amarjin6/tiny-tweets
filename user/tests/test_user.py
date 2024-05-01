import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from django.urls import reverse
from user.tests.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_user(api_client):
    url = reverse('api_v1:user-list')
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_retrieve_user(api_client):
    user = UserFactory(role='moderator')

    api_client.force_authenticate(user=user)

    url = reverse('api_v1:user-detail', kwargs={'pk': user.pk})
    response = api_client.get(url)

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_update_user(api_client):
    user = UserFactory(role='moderator')
    url = reverse('api_v1:user-detail', kwargs={'pk': user.pk})
    api_client.force_authenticate(user=user)
    data = {
        'id': user.pk,
        'first_name': 'Updated',
        'last_name': 'User',
        'email': user.email,
        'password': user.password,
        'username': user.username,
    }
    response = api_client.patch(url, data, format='json')

    assert response.status_code == HTTP_200_OK
    assert response.data['first_name'] == 'Updated'


@pytest.mark.django_db
def test_delete_user(api_client):
    user = UserFactory(role='admin', is_staff=True)
    url = reverse('api_v1:user-detail', kwargs={'pk': user.pk})
    api_client.force_authenticate(user=user)
    response = api_client.delete(url)
    assert response.status_code == HTTP_204_NO_CONTENT

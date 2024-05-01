import pytest
from rest_framework.reverse import reverse

from user.tests.factories import UserFactory


@pytest.mark.django_db
def test_get_user_own_info(api_client):
    some_user = UserFactory(role='moderator')
    api_client.force_authenticate(user=some_user)
    user_detail_url = reverse('api_v1:User-detail', kwargs={'pk': some_user.id})
    response = api_client.get(user_detail_url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_name, status_code', [
        pytest.param(
            'api_client',
            401,
            id='no_authentication_no_access'
        ),
        pytest.param(
            'moderator_api_client',
            200,
            id='user_account'
        ),
        pytest.param(
            'moderator_api_client',
            200,
            id='moderator_account'
        ),
        pytest.param(
            'admin_api_client',
            200,
            id='admin_account_with_full_access'
        ),
    ]
)
def test_get_another_user_info(request, client_name, status_code):
    some_user = UserFactory()
    url = reverse('api_v1:User-detail', kwargs={'pk': some_user.id})
    api_client = request.getfixturevalue(client_name)
    response = api_client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_name, status_code', [
        pytest.param(
            'api_client',
            401,
            id='no_authentication_no_access'
        ),
        pytest.param(
            'moderator_api_client',
            200,
            id='user_account'
        ),
        pytest.param(
            'moderator_api_client',
            200,
            id='moderator_account'
        ),
        pytest.param(
            'admin_api_client',
            200,
            id='admin_account_with_full_access'
        ),
    ]
)
def test_get_users_list(request, client_name, status_code):
    url = reverse('api_v1:User-list')
    api_client = request.getfixturevalue(client_name)
    response = api_client.get(url)
    assert response.status_code == status_code

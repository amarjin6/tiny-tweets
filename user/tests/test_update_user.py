import pytest
from rest_framework.reverse import reverse

from user.tests.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    'patch_data', [
        {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
        },
        {
            'last_name': 'Ivanov',
        },
        {
            'username': 'test1',
            'email': 'test1@gmail.com'
        },
{
            'last_name': 'Ivan',
        },
        {
            'username': 'test',
            'email': 'test@gmail.com'
        },
    ]
)
def test_update_user_own_info(api_client, patch_data):
    some_user = UserFactory()
    api_client.force_authenticate(some_user)
    data = {
        'id': some_user.pk,
        'email': some_user.email,
        'password': some_user.password,
        'username': some_user.username,
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
    }
    user_detail_url = reverse('api_v1:user-detail', kwargs={'pk': some_user.id})
    response = api_client.patch(user_detail_url, data=data)
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
            'user_api_client',
            200,
            id='user_account_with_no_access'
        ),
        pytest.param(
            'moderator_api_client',
            200,
            id='moderator_account_with_no_access'
        ),
        pytest.param(
            'admin_api_client',
            200,
            id='admin_account_with_full_access'
        ),
    ]
)
def test_update_another_user_info(request, client_name, status_code):
    some_user = UserFactory()
    url = reverse('api_v1:user-detail', kwargs={'pk': some_user.id})
    api_client = request.getfixturevalue(client_name)
    patch_data = {
        'id': some_user.pk,
        'email': some_user.email,
        'username': some_user.username,
        'first_name': 'Ivan',
        'last_name': 'Ivanov',
    }
    response = api_client.patch(url, data=patch_data)
    assert response.status_code == status_code

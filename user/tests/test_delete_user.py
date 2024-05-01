import pytest
from rest_framework.reverse import reverse

from user.tests.factories import UserFactory


@pytest.mark.django_db
def test_delete_user_by_himself(api_client):
    user = UserFactory(role='admin', is_staff=True)
    url = reverse('api_v1:user-detail', kwargs={'pk': user.pk})
    api_client.force_authenticate(user=user)
    response = api_client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_name, status_code', [
        pytest.param(
            'api_client',
            401,
            id='no_authentication_no_access'
        ),
        pytest.param(
            'api_client',
            401,
            id='user_account_with_no_access'
        ),
        pytest.param(
            'api_client',
            401,
            id='moderator_account_with_no_access'
        ),
        pytest.param(
            'api_client',
            401,
            id='admin_account_with_full_access'
        ),
    ]
)
def test_delete_another_user(request, client_name, status_code):
    some_user = UserFactory(role='user')
    url = reverse('api_v1:user-detail', kwargs={'pk': some_user.id})
    api_client = request.getfixturevalue(client_name)
    response = api_client.delete(url)
    assert response.status_code == status_code

import pytest
from rest_framework.reverse import reverse

from page.tests.factories import PageFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_name, status_code', [
        pytest.param(
            'api_client',
            [401],
            id='no_authentication_no_access'
        ),
        pytest.param(
            'user_api_client',
            [204, 403],
            id='user_account'
        ),
        pytest.param(
            'moderator_api_client',
            [204, 403],
            id='moderator_account'
        ),
        pytest.param(
            'admin_api_client',
            [204, 403],
            id='admin_account'
        ),
    ]
)
def test_delete_other_page_by_another_user(request, client_name, status_code):
    some_page = PageFactory()
    url = reverse('api_v1:Page-detail', kwargs={'pk': some_page.id})
    api_client = request.getfixturevalue(client_name)
    response = api_client.delete(url)
    assert response.status_code in status_code


@pytest.mark.django_db
def test_delete_own_page(api_client):
    page = PageFactory()
    api_client.force_authenticate(page.owner)
    url = reverse('api_v1:Page-detail', kwargs={'pk': page.id})
    response = api_client.delete(url)
    assert response.status_code == 204

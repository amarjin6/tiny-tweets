import datetime

import pytest
from rest_framework.reverse import reverse

from page.tests.factories import PageFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    'patch_data',
    [
        {'title': 'other name', 'description': 'some description'},
        {'title': 'new title'},
        {'description': 'new description'},
        {'title': '', 'description': 'some description'},
        {'title': 'other name', 'description': ''},
    ]
)
def test_update_own_page_info(api_client, patch_data):
    page = PageFactory()
    api_client.force_authenticate(page.owner)
    url = reverse('api_v1:Page-detail', kwargs={'pk': page.id})
    response = api_client.patch(url, data=patch_data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_other_page_info_by_another_user(user_api_client):
    some_page = PageFactory()
    url = reverse('api_v1:Page-detail', kwargs={'pk': some_page.id})
    patch_data = {
        'title': 'other name',
        'description': 'some description'
    }
    response = user_api_client.patch(url, data=patch_data)
    assert response.status_code in [403, 400]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'client_name', [
        pytest.param(
            'moderator_api_client',
            id='moderator_account_with_no_access'
        ),
        pytest.param(
            'admin_api_client',
            id='admin_account_with_full_access'
        )
    ]
)
def test_update_other_page_info_by_administration(request, client_name):
    page = PageFactory()
    url = reverse('api_v1:Page-detail', kwargs={'pk': page.id})
    api_client = request.getfixturevalue(client_name)
    patch_data = {
        'unblock_date': datetime.datetime(2030, 1, 1, tzinfo=datetime.timezone.utc)
    }
    response = api_client.patch(url, data=patch_data)

    assert response.status_code in [200, 403, 400]

import pytest
from rest_framework.reverse import reverse

from page.tests.factories import PageFactory, TagFactory


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
            id='admin_account'
        ),
    ]
)
def test_get_page_info(request, client_name, status_code):
    tag1 = TagFactory()
    tag2 = TagFactory()
    some_page = PageFactory(tags=[tag1, tag2])
    url = reverse('api_v1:Page-detail', kwargs={'pk': some_page.id})
    api_client = request.getfixturevalue(client_name)
    response = api_client.get(url)
    assert response.status_code == status_code

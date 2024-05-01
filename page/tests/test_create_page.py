import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'post_data, status_code', [
        pytest.param(
            {},
            401,
            id='no_data'
        ),
        pytest.param(
            {
                'title': ''
            },
            401,
            id='blank_name'
        ),
        pytest.param(
            {
                'title': 'name',
                'is_private': True
            },
            401,
            id='invalid_image'
        ),
    ]
)
def test_create_page_without_authentication(api_client, post_data, status_code):
    url = reverse('api_v1:Page-list')
    response = api_client.post(url, data=post_data)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'post_data, status_code', [
        pytest.param(
            {},
            400,
            id='no_data'
        ),
        pytest.param(
            {
                'title': ''
            },
            400,
            id='blank_name'
        ),
        pytest.param(
            {
                'title': 'name',
                'is_private': True
            },
            400,
            id='invalid_image'
        ),
    ]
)
def test_create_page_with_image(user_api_client, post_data, status_code):
    url = reverse('api_v1:Page-list')
    response = user_api_client.post(url, data=post_data)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'post_data, status_code', [
        pytest.param(
            {
                'title': 'some_name',
                'tags': ['tinytag', 'tinytag4', 'newbie', 'hello']
            },
            400,
            id='valid_post_with_repetetive_tags'
        ),
        pytest.param(
            {
                'title': 'another_name',
                'uuid': 'very_unique_id',
                'tags': []
            },
            400,
            id='valid_post_with_no_tags'
        ),
        pytest.param(
            {
                'title': 'another_name',
                'uuid': 'very_unique_id',
                'is_private': True,
                'tags': 'tag1'
            },
            400,
            id='invalid_tags_form'
        )

    ]
)
def test_create_page_with_tags(user_api_client, post_data, status_code):
    url = reverse('api_v1:Page-list')
    response = user_api_client.post(url, data=post_data, format='json')
    assert response.status_code == status_code

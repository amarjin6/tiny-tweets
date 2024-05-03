import pytest
from rest_framework.reverse import reverse

from page.tests.factories import PageFactory, PostFactory
from user.tests.factories import UserFactory


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
                'content': 'tiny content'
            },
            400,
            id='only_content'
        ),
        pytest.param(
            {
                'content': 'tiny content',
                'reply_to': 228
            },
            400,
            id='content_with_invalid_reply'
        ),
    ]
)
def test_create_post_without_page(user_api_client, post_data, status_code):
    url = reverse('api_v1:post-list')
    response = user_api_client.post(url, data=post_data)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_create_post_on_another_page(api_client):
    some_user = UserFactory()
    page = PageFactory()
    api_client.force_authenticate(some_user)
    api_client.force_login(some_user)
    url = reverse('api_v1:post-list')
    post_data = {
        'page': page.id,
        'content': 'Some content'
    }
    response = api_client.post(url, data=post_data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_post_on_own_page(api_client):
    some_user = UserFactory()
    page = PageFactory(owner=some_user)
    api_client.force_authenticate(some_user)
    api_client.force_login(some_user)
    url = reverse('api_v1:post-list')
    post_data = {
        'page': page.pk,
        'content': 'Some content',
    }
    response = api_client.post(url, data=post_data)
    assert response.status_code in [201, 400]


@pytest.mark.django_db
def test_create_post_on_own_page_with_reply(api_client):
    some_user = UserFactory()
    random_post = PostFactory()
    page = PageFactory(owner=some_user)
    api_client.force_authenticate(some_user)
    url = reverse('api_v1:post-list')
    post_data = {
        'page': page.id,
        'content': 'Some content',
        'reply_to': random_post.id
    }
    response = api_client.post(url, data=post_data)
    assert response.status_code in [201, 400]

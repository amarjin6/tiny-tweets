import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'post_data, status_code', [
        pytest.param(
            {
                'email': 'test@gmail.com',
            },
            400,
            id='only_valid_email'
        ),
        pytest.param(
            {
                'email': 'test@gmail.com',
                'username': 'test',
            },
            400,
            id='no_password'
        ),
        pytest.param(
            {
                'email': 'test@gmail.com',
                'password': '123'
            },
            400,
            id='no_password'
        ),
        pytest.param(
            {
                'email': 'gmail.com',
                'username': 'test',
                'password': 123
            },
            400,
            id='invalid_email'
        ),
        pytest.param(
            {
                'email': 'user@gmail.com',
                'username': 'test',
                'password': '123test_password',
                'first_name': 'Test',
                'last_name': 'User',
            },
            201,
            id='valid_data'
        ),
        pytest.param(
            {
                'email': 'user@gmail.com',
                'username': 'test',
                'password': '123_test_password123',
                'first_name': 'Test',
                'last_name': 'User',
                'role': 'user'
            },
            201,
            id='valid_data_with_jpg'
        ),
        pytest.param(
            {
                'email': 'user@gmail.com',
                'username': 'test',
                'password': 123,
                'image': 'iam_image:3'
            },
            400,
            id='valid_data_with_invalid_image_field'
        ),
    ]
)
def test_create_user(api_client, post_data, status_code):
    url = reverse('api_v1:user-list')
    response = api_client.post(url, data=post_data)
    assert response.status_code == status_code

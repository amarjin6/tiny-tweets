import os
import pytest
from rest_framework.test import APIClient

from user.models import User
from user.tests.factories import UserFactory


@pytest.fixture
def aws_credentials():
    os.environ["AWS_S3_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_S3_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_api_client():
    client = APIClient()
    user: User = UserFactory(role='admin')
    client.force_authenticate(user=user)

    return client


@pytest.fixture
def moderator_api_client():
    client = APIClient()
    user: User = UserFactory(role='moderator')
    client.force_authenticate(user=user)

    return client


@pytest.fixture
def user_api_client():
    client = APIClient()
    user: User = UserFactory(role='user')
    client.force_authenticate(user=user)

    return client

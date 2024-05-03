import factory
from factory.django import DjangoModelFactory

from user.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    image = factory.Faker('image_url')
    is_staff = factory.Faker('pybool')
    role = 'user'

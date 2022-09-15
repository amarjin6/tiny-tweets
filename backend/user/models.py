from django.db import models
from django.contrib.auth.models import AbstractUser

from core.enums import Role


class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Role.choices(), default=Role.USER.value, blank=False)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        name = self.username
        if self.role == Role.USER.value:
            name = f'user {name}'

        elif self.role == Role.MODERATOR.value:
            name = f'moderator {name}'

        elif self.role == Role.ADMIN.value:
            name = f'admin {name}'

        return name

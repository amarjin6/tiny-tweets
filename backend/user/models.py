from django.db import models
from django.contrib.auth.models import AbstractUser

from core.enums import Role
from user.managers import CustomUserManager


class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Role.choices(), default=Role.USER.value, blank=False)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def __str__(self):
        email = self.email
        if self.role == Role.USER.value:
            email = f'user {email}'

        elif self.role == Role.MODERATOR.value:
            email = f'moderator {email}'

        elif self.role == Role.ADMIN.value:
            email = f'admin {email}'

        return email

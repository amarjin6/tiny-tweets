from django.db import models
from django.contrib.auth.models import AbstractUser

from core.enums import Role
from user.managers import CustomUserManager


class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Role.choices(), default=Role.USER.value, blank=False)
    is_blocked = models.BooleanField(default=False)
    last_update = models.DateTimeField(blank=True, auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = CustomUserManager()

    def __str__(self):
        name = self.username
        if self.role == Role.USER.value:
            name = f'user {name}'

        elif self.role == Role.MODERATOR.value:
            name = f'moderator {name}'

        elif self.role == Role.ADMIN.value:
            name = f'admin {name}'

        return name

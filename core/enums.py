from enum import Enum


class Role(Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    @classmethod
    def choices(cls):
        return [(attr.value, attr.name) for attr in cls]

    def __str__(self):
        return self.value

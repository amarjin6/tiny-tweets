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


class AWSClient(Enum):
    SES_CLIENT = 'ses_client',
    S3_CLIENT = 's3_client'
    S3_RESOURCE = 's3_resource'

    def __str__(self):
        return self.value

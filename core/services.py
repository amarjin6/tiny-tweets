import boto3
import os
from botocore.exceptions import ClientError
import logging

from page.models import Page
from user.models import User


class AWSMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AWSManager(metaclass=AWSMeta):
    def __init__(self):
        self.credentials = {
            'endpoint_url': f"http://{os.getenv('HOSTNAME_EXTERNAL')}:"
                            f"{os.getenv('PORT_EXTERNAL')}",
            'region_name': os.getenv('AWS_DEFAULT_REGION'),
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY')
        }

        self.s3 = boto3.resource(
            's3',
            endpoint_url=self.credentials['endpoint_url'],
            region_name=self.credentials['region_name'],
            aws_access_key_id=self.credentials['aws_access_key_id'],
            aws_secret_access_key=self.credentials['aws_secret_access_key']
        )

        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.credentials['endpoint_url'],
            region_name=self.credentials['region_name'],
            aws_access_key_id=self.credentials['aws_access_key_id'],
            aws_secret_access_key=self.credentials['aws_secret_access_key']
        )

        self.ses_client = boto3.client(
            'ses',
            endpoint_url=self.credentials['endpoint_url'],
            region_name=self.credentials['region_name'],
            aws_access_key_id=self.credentials['aws_access_key_id'],
            aws_secret_access_key=self.credentials['aws_secret_access_key']
        )

        self.ses_client.verify_email_identity(EmailAddress=os.getenv('EMAIL_HOST_USER'))

        try:
            self.bucket = self.s3.create_bucket(
                Bucket=os.getenv('BUCKET_NAME'),
                CreateBucketConfiguration={
                    'LocationConstraint': os.getenv('AWS_DEFAULT_REGION')
                }
            )
        except self.s3_client.exceptions.BucketAlreadyOwnedByYou:
            self.bucket = self.s3.Bucket(name=os.getenv('BUCKET_NAME'))

    def create_presigned_url(self, key: str, expiration: int = int(os.getenv('EXPIRATION_TIME')),
                             bucket: str = os.getenv('BUCKET_NAME')) -> str | None:
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket,
                        'Key': key},
                ExpiresIn=expiration
            )

        except ClientError as e:
            logging.error(e)
            return None

        return response.replace('http://localstack', 'http://0.0.0.0')

    def upload_file(self, file_path: str, key: str) -> str:
        with open(file_path, 'rb') as data:
            self.bucket.put_object(Key=key, Body=data)

        return key

    def send_mail(self, data: list) -> dict:
        emails_list = list(Page.objects.values_list('followers__email', flat=True).distinct().filter(id=data['page']))
        owner = User.objects.get(id=data['owner'])
        msg = f"User {owner.username} created a new post: {data['content']}"
        response = self.ses_client.send_email(
            Source=os.getenv('EMAIL_HOST_USER'),
            Destination={
                'ToAddresses': emails_list
            },
            Message={
                'Subject': {
                    'Data': os.getenv('SUBJECT'),
                },
                'Body': {
                    'Text': {
                        'Data': msg,
                    },
                    'Html': {
                        'Data': '<h1>' + msg + '</h1>',
                    }
                }
            }
        )

        return response

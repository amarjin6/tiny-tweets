import boto3
import os
from celery import shared_task
from botocore.exceptions import ClientError
import logging

from page.models import Page
from user.models import User


class AWSManagerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AWSManager(metaclass=AWSManagerMeta):
    def __init__(self):
        self.credentials = {'endpoint_url': f"http://{os.getenv('HOSTNAME_EXTERNAL', 'localstack')}:"
                                            f"{os.getenv('PORT_EXTERNAL', '4566')}",
                            'region_name': str(os.getenv('AWS_DEFAULT_REGION')),
                            'aws_access_key_id': str(os.getenv('AWS_ACCESS_KEY_ID')),
                            'aws_secret_access_key': str(os.getenv('AWS_SECRET_KEY'))}

        self.s3 = boto3.resource('s3', endpoint_url=self.credentials['endpoint_url'],
                                 region_name=self.credentials['region_name'],
                                 aws_access_key_id=self.credentials['aws_access_key_id'],
                                 aws_secret_access_key=self.credentials['aws_secret_access_key'])

        self.s3_client = boto3.client('s3', endpoint_url=self.credentials['endpoint_url'],
                                      region_name=self.credentials['region_name'],
                                      aws_access_key_id=self.credentials['aws_access_key_id'],
                                      aws_secret_access_key=self.credentials['aws_secret_access_key'])

        self.ses_client = boto3.client('ses', endpoint_url=self.credentials['endpoint_url'],
                                       region_name=self.credentials['region_name'],
                                       aws_access_key_id=self.credentials['aws_access_key_id'],
                                       aws_secret_access_key=self.credentials['aws_secret_access_key'])
        try:
            self.bucket = self.s3.create_bucket(Bucket=os.getenv('BUCKET_NAME', 'images'), CreateBucketConfiguration={
                'LocationConstraint': os.getenv('AWS_DEFAULT_REGION', 'us-west-2')})
        except self.s3_client.exceptions.BucketAlreadyOwnedByYou:
            self.bucket = self.s3.Bucket(name=os.getenv('BUCKET_NAME', 'images'))

    def create_presigned_url(self, key: str, expiration=86400,
                             bucket: str = os.getenv('BUCKET_NAME', 'images')) -> str | None:
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': bucket,
                                                                     'Key': key},
                                                             ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None

        return response.replace('http://localstack', 'http://0.0.0.0')

    def upload_file(self, file_path: str, key: str) -> str:
        with open(file_path, 'rb') as data:
            self.bucket.put_object(Key=key, Body=data)

        return key

    @shared_task
    def send_mail(self, data: list) -> dict:
        self.ses_client.verify_email_identity(EmailAddress=os.getenv('EMAIL_HOST_USER'))
        followers = Page.objects.get(id=data['page']).followers.all()
        emails_list = [follower.email for follower in followers]
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

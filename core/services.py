import boto3
import os
from botocore.exceptions import ClientError
import logging
from functools import lru_cache

from page.models import Page
from user.models import User
from core.enums import AWSClient


class AWSManager:
    @staticmethod
    @lru_cache
    def get_client(client_name: str):
        credentials = {
            'endpoint_url': f"http://{os.getenv('HOSTNAME_EXTERNAL')}:"
                            f"{os.getenv('PORT_EXTERNAL')}",
            'region_name': os.getenv('AWS_DEFAULT_REGION'),
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY')
        }

        entity = None

        if client_name == AWSClient.S3_CLIENT.value:
            s3_client = boto3.client(
                's3',
                endpoint_url=credentials['endpoint_url'],
                region_name=credentials['region_name'],
                aws_access_key_id=credentials['aws_access_key_id'],
                aws_secret_access_key=credentials['aws_secret_access_key']
            )

            entity = s3_client

        elif client_name == AWSClient.SES_CLIENT.value:
            ses_client = boto3.client(
                'ses',
                endpoint_url=credentials['endpoint_url'],
                region_name=credentials['region_name'],
                aws_access_key_id=credentials['aws_access_key_id'],
                aws_secret_access_key=credentials['aws_secret_access_key']
            )

            ses_client.verify_email_identity(EmailAddress=os.getenv('EMAIL_HOST_USER'))
            entity = ses_client

        elif client_name == AWSClient.S3_RESOURCE.value:
            s3_resource = boto3.resource(
                's3',
                endpoint_url=credentials['endpoint_url'],
                region_name=credentials['region_name'],
                aws_access_key_id=credentials['aws_access_key_id'],
                aws_secret_access_key=credentials['aws_secret_access_key']
            )

            entity = s3_resource

        return entity

    @staticmethod
    @lru_cache
    def get_bucket(bucket_name: str):
        s3_client = AWSManager.get_client(AWSClient.S3_CLIENT.value)

        try:
            bucket = s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': os.getenv('AWS_DEFAULT_REGION')
                }
            )
        except s3_client.exceptions.BucketAlreadyOwnedByYou:
            s3_resource = AWSManager.get_client(AWSClient.S3_RESOURCE.value)
            bucket = s3_resource.Bucket(name=os.getenv('BUCKET_NAME'))

        return bucket

    @staticmethod
    def create_presigned_url(key: str, expiration: int = int(os.getenv('EXPIRATION_TIME')),
                             bucket: str = os.getenv('BUCKET_NAME')) -> str | None:
        s3_client = AWSManager.get_client(AWSClient.S3_CLIENT.value)

        try:
            response = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket,
                        'Key': key},
                ExpiresIn=expiration
            )

        except ClientError as e:
            logging.error(e)
            return None

        return response.replace('http://localstack', 'http://0.0.0.0')

    @staticmethod
    def upload_file(file_path: str, key: str) -> str:
        bucket = AWSManager.get_bucket(os.getenv('BUCKET_NAME'))

        with open(file_path, 'rb') as data:
            bucket.put_object(Key=key, Body=data)

        return key

    @staticmethod
    def send_mail(data: list) -> dict:
        emails_list = list(Page.objects.values_list('followers__email', flat=True).distinct().filter(id=data['page']))
        owner = User.objects.get(id=data['owner'])
        msg = f"User {owner.username} created a new post: {data['content']}"
        ses_client = AWSManager.get_client(AWSClient.SES_CLIENT.value)

        response = ses_client.send_email(
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

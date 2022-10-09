import boto3
import os

from page.models import Page
from user.models import User


class AWSManager:
    @staticmethod
    def upload_file(file_path: str):
        s3 = boto3.resource('s3',
                            endpoint_url=f"http://{os.getenv('HOSTNAME_EXTERNAL', 'localstack')}:"
                                         f"{os.getenv('PORT_EXTERNAL', '4566')}",
                            region_name=str(os.getenv('AWS_DEFAULT_REGION')),
                            aws_access_key_id=str(os.getenv('AWS_ACCESS_KEY_ID')),
                            aws_secret_access_key=str(os.getenv('AWS_SECRET_KEY')))

        bucket = s3.create_bucket(Bucket='images', CreateBucketConfiguration={
            'LocationConstraint': os.getenv('AWS_DEFAULT_REGION', 'us-west-2')})
        with open(file_path, 'rb') as data:
            file_name = file_path.split('.')[0].split('/')[-1] + '.' + file_path.split('.')[-1]
            bucket.put_object(Key=file_name, Body=data)

    @staticmethod
    def send_mail(data: list) -> dict:
        client = boto3.client('ses',
                              endpoint_url=f"http://{os.getenv('HOSTNAME_EXTERNAL', 'localstack')}:"
                                           f"{os.getenv('PORT_EXTERNAL', '4566')}",
                              region_name=str(os.getenv('AWS_DEFAULT_REGION')),
                              aws_access_key_id=str(os.getenv('AWS_ACCESS_KEY_ID')),
                              aws_secret_access_key=str(os.getenv('AWS_SECRET_KEY')))

        client.verify_email_identity(EmailAddress=os.getenv('EMAIL_HOST_USER'))
        followers = Page.objects.get(id=data['page']).followers.all()
        emails_list = [follower.email for follower in followers]
        owner = User.objects.get(id=data['owner'])
        msg = f"User {owner.username} created a new post: {data['content']}"
        response = client.send_email(
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

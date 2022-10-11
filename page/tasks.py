from celery import shared_task
from core.services import AWSManager


@shared_task()
def send_mail(data: list) -> dict:
    aws = AWSManager()
    return aws.send_mail(data)

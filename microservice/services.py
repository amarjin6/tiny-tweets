import boto3
import os
from functools import lru_cache


class AWSManager:
    @staticmethod
    @lru_cache
    def get_table():
        credentials = {
            'endpoint_url': f"http://{os.getenv('HOSTNAME_EXTERNAL')}:"
                            f"{os.getenv('PORT_EXTERNAL')}",
            'region_name': os.getenv('AWS_DEFAULT_REGION'),
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY')
        }

        dynamodb_client = boto3.client(
            "dynamodb",
            endpoint_url=credentials['endpoint_url'],
            region_name=credentials['region_name'],
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key']
        )

        try:
            table = dynamodb_client.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'N'
                    },
                ],
                TableName=os.getenv('AWS_DYNAMODB_TABLE_NAME'),
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    },
                ],

                BillingMode='PAY_PER_REQUEST',
            )

        except dynamodb_client.exceptions.ResourceInUseException:
            dynamodb_resource = boto3.resource(
                "dynamodb",
                endpoint_url=credentials['endpoint_url'],
                region_name=credentials['region_name'],
                aws_access_key_id=credentials['aws_access_key_id'],
                aws_secret_access_key=credentials['aws_secret_access_key']
            )

            table = dynamodb_resource.Table(os.getenv('AWS_DYNAMODB_TABLE_NAME'))

        return table


class StatisticsService:
    @staticmethod
    def get_statistics():
        table = AWSManager.get_table()
        return table

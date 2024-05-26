import boto3
import os
from functools import lru_cache
from fastapi import HTTPException
from typing import Dict, Any


class AWSManager:
    @staticmethod
    @lru_cache
    def get_credentials() -> dict:
        credentials = {
            'endpoint_url': f"http://{os.getenv('HOSTNAME_EXTERNAL')}:"
                            f"{os.getenv('PORT_EXTERNAL')}",
            'region_name': os.getenv('AWS_DEFAULT_REGION'),
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_KEY')
        }

        return credentials

    @staticmethod
    @lru_cache
    def get_client(client_name: str):
        credentials = AWSManager.get_credentials()
        client = boto3.client(
            client_name,
            endpoint_url=credentials['endpoint_url'],
            region_name=credentials['region_name'],
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key']
        )

        return client

    @staticmethod
    @lru_cache
    def get_resource(resource_name: str):
        credentials = AWSManager.get_credentials()
        resource = boto3.resource(
            resource_name,
            endpoint_url=credentials['endpoint_url'],
            region_name=credentials['region_name'],
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key']
        )

        return resource

    @staticmethod
    @lru_cache
    def get_table():
        dynamodb_client = AWSManager.get_client('dynamodb')
        dynamodb_resource = AWSManager.get_resource('dynamodb')

        try:
            table = dynamodb_client.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': 'Page',
                        'AttributeType': 'S'
                    },
                ],
                TableName=os.getenv('AWS_DYNAMODB_TABLE_NAME'),
                KeySchema=[
                    {
                        'AttributeName': 'Page',
                        'KeyType': 'HASH'
                    },
                ],

                BillingMode='PAY_PER_REQUEST',
            )

        except dynamodb_client.exceptions.ResourceInUseException:

            table = dynamodb_resource.Table(os.getenv('AWS_DYNAMODB_TABLE_NAME'))

        return table

    @staticmethod
    def get_item():
        table = AWSManager.get_table()
        response = table.scan()

        items = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return items

    @staticmethod
    def put_item(page: dict):
        table = AWSManager.get_table()
        response = table.put_item(
            Item={
                'Page': str(page),
            }
        )

        return response

    @staticmethod
    def delete_item(page: dict):
        table = AWSManager.get_table()
        response = table.delete_item(
            Item={
                'Page': str(page),
            }
        )

        return response

    @staticmethod
    def update_item(page: str):
        table = AWSManager.get_table()
        response = table.update_item(
            Item={
                'Page': str(page),
            }
        )

        return response


class StatisticsService:
    @staticmethod
    def get_statistics():
        pages = AWSManager.get_item()
        statistics = []

        for page_item in pages:
            page = eval(page_item['Page'])

            page_id = page['id']
            uuid = page['uuid']
            title = page['title']
            description = page['description']
            tags = page['tags']
            is_private = page['is_private']

            tags_count = len(tags)
            description_length = len(description)
            title_length = len(title)
            total_length = tags_count + description_length + title_length
            privacy_status = 'Private' if is_private else 'Public'

            page_statistics = {
                'id': page_id,
                'uuid': uuid,
                'title': title,
                'description': description,
                'tags_count': tags_count,
                'description_length': description_length,
                'title_length': title_length,
                'total_length': total_length,
                'privacy_status': privacy_status,
            }

            statistics.append(page_statistics)

        return statistics

    @staticmethod
    def get_statistics_by_id(page_id: int) -> Dict[str, Any]:
        pages = AWSManager.get_item()
        for page_item in pages:
            page = eval(page_item['Page'])

            if page['id'] == page_id:
                uuid = page['uuid']
                title = page['title']
                description = page['description']
                tags = page['tags']
                is_private = page['is_private']

                tags_count = len(tags)
                description_length = len(description)
                title_length = len(title)
                total_length = tags_count + description_length + title_length
                privacy_status = 'Private' if is_private else 'Public'

                page_statistics = {
                    'id': page_id,
                    'uuid': uuid,
                    'title': title,
                    'description': description,
                    'tags_count': tags_count,
                    'description_length': description_length,
                    'title_length': title_length,
                    'total_length': total_length,
                    'privacy_status': privacy_status,
                }

                return page_statistics

        raise HTTPException(status_code=404, detail='Page not found')

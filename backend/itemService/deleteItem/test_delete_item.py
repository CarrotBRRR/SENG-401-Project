import pytest
from main import *
from moto import mock_aws
import boto3
from decimal import Decimal



@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

@pytest.fixture
def dynamodb_mock(aws_credentials):
    with mock_aws():
        yield boto3.resource('dynamodb', region_name='ca-central-1')

@pytest.fixture
def items_table(dynamodb_mock):
    """Create a mock DynamoDB table."""
    table = dynamodb_mock.create_table(
        TableName='items-30144999',
        KeySchema=[
            {'AttributeName': 'itemID', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'location', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'N'},
            {'AttributeName': 'itemID', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'LocationTimestampIndex',
                'KeySchema': [
                    {'AttributeName': 'location', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'} 
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            }
        ]
    )
    return table


def test_remove_item(items_table):
    items_table.put_item(Item={'itemID': '1', 'location': 'Los Angeles', 'timestamp': Decimal('123')})
    items_table.put_item(Item={'itemID': '2', 'location': 'Los Angeles', 'timestamp': Decimal('123.1')})

    remove_item(items_table, '1')
    response = items_table.scan()
    items = response['Items']
    assert len(items) == 1
    assert items[0]['itemID'] == '2'

    remove_item(items_table, '2')
    response = items_table.scan()
    items = response['Items']
    assert len(items) == 0





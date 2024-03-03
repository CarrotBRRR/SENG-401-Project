import pytest
from moto import mock_aws
import boto3
import json
from main import *

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
            {'AttributeName': 'itemID', 'AttributeType': 'S'},
            {'AttributeName': 'lenderID', 'AttributeType': 'S'}
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
            },
            {
                'IndexName': 'LenderIDIndex',
                'KeySchema': [
                    {'AttributeName': 'lenderID', 'KeyType': 'HASH'},
                    {'AttributeName': 'itemID', 'KeyType': 'RANGE'}
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

def test_get_items_by_lender_id(items_table):
    items_table.put_item(
        Item={
            'itemID': '1',
            'lenderID': '2',
            'itemName': 'item1',
            'description': 'description1',
            'condition': 'condition1',
            'category': 'category1',
            'location': 'location1',
            'timestamp': 1
        }
    )
    items_table.put_item(
        Item={
            'itemID': '2',
            'lenderID': '2',
            'itemName': 'item2',
            'description': 'description2',
            'condition': 'condition2',
            'category': 'category2',
            'location': 'location2',
            'timestamp': 2
        }
    )
    items_table.put_item(
        Item={
            'itemID': '3',
            'lenderID': '3',
            'itemName': 'item3',
            'description': 'description3',
            'condition': 'condition3',
            'category': 'category3',
            'location': 'location3',
            'timestamp': 3
        }
    )
    response = get_items_by_lender_id(items_table, '2', 'LenderIDIndex')
    assert response == [
        {
            'itemID': '1',
            'lenderID': '2',
            'itemName': 'item1',
            'description': 'description1',
            'condition': 'condition1',
            'category': 'category1',
            'location': 'location1',
            'timestamp': 1
        },
        {
            'itemID': '2',
            'lenderID': '2',
            'itemName': 'item2',
            'description': 'description2',
            'condition': 'condition2',
            'category': 'category2',
            'location': 'location2',
            'timestamp': 2
        }
    ]

def test_handler(items_table):
    items_table.put_item(
        Item={
            'itemID': '1',
            'lenderID': '2',
            'itemName': 'item1',
            'description': 'description1',
            'condition': 'condition1',
            'category': 'category1',
            'location': 'location1',
            'timestamp': 1
        }
    )
    items_table.put_item(
        Item={
            'itemID': '2',
            'lenderID': '2',
            'itemName': 'item2',
            'description': 'description2',
            'condition': 'condition2',
            'category': 'category2',
            'location': 'location2',
            'timestamp': 2
        }
    )
    event = {
        'headers': {'lenderid': '2'}
    }
    response = handler(event, None)
    

    assert response['statusCode'] == 200
    items = json.loads(response['body'])['items']
    assert items == [
        {
            'itemID': '1',
            'lenderID': '2',
            'itemName': 'item1',
            'description': 'description1',
            'condition': 'condition1',
            'category': 'category1',
            'location': 'location1',
            'timestamp': 1
        },
        {
            'itemID': '2',
            'lenderID': '2',
            'itemName': 'item2',
            'description': 'description2',
            'condition': 'condition2',
            'category': 'category2',
            'location': 'location2',
            'timestamp': 2
        }
    ]
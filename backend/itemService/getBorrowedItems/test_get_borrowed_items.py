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
            {'AttributeName': 'borrowerID', 'AttributeType': 'S'}
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
                'IndexName': 'BorrowerIDIndex',
                'KeySchema': [
                    {'AttributeName': 'borrowerID', 'KeyType': 'HASH'},
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

def test_get_items_by_borrower_id(items_table):
    table = items_table
    table.put_item(
        Item={
            'itemID': '1',
            'name': 'test item',
            'description': 'test description',
            'lenderID': 'lender1',
            'borrowerID': 'borrower1'
        }
    )
    table.put_item(
        Item={
            'itemID': '2',
            'name': 'test item 2',
            'description': 'test description 2',
            'lenderID': 'lender2',
        }
    )
    table.put_item(
        Item={
            'itemID': '3',
            'name': 'test item 3',
            'description': 'test description 3',
            'lenderID': 'lender3',
            'borrowerID': 'borrower1'
        }
    )

    items = get_items_by_borrower_id(table, 'borrower1', 'BorrowerIDIndex')
    assert len(items) == 2
    assert items[0]['itemID'] == '1'
    assert items[1]['itemID'] == '3'
    assert items[0]['name'] == 'test item'
    assert items[1]['name'] == 'test item 3'
    assert items[0]['description'] == 'test description'

def test_get_items_by_borrower_id_no_borrower_id(items_table):
    table = items_table
    response = get_items_by_borrower_id(table, '', 'BorrowerIDIndex')
    assert response == []

def test_get_items_by_borrower_id_no_items(items_table):
    table = items_table
    response = get_items_by_borrower_id(table, 'borrower1', 'BorrowerIDIndex')
    assert response == []

def test_handler_no_borrower_id():
    event = {
        "headers": {
            "borrowerid": ""
        }
    }
    response = handler(event, {})
    assert response == {
        'statusCode': 400,
        'body': json.dumps({
            'error': 'No borrowerID provided'
        })
    }

    
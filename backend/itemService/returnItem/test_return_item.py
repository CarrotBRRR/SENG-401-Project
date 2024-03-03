import pytest
import boto3
from moto import mock_aws
from main import *

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'

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

def test_parse_event_body_with_dict():
    event_body = {"key": "value"}
    assert parse_event_body(event_body) == event_body

def test_parse_event_body_with_json_string():
    event_body = '{"key": "value"}'
    expected_result = {"key": "value"}
    assert parse_event_body(event_body) == expected_result

def test_remove_borrowerID_from_item(items_table):
    item = {
        'itemID': '1',
        'location': 'Vancouver',
        'timestamp': 123456789,
        'borrowerID': 'user1'
    }
    table = items_table
    table.put_item(Item=item)
    response = update_borrowerID_to_null_in_item(table, '1')
    assert response['Attributes']['borrowerID'] == None

def test_handler(items_table):
    item = {
        'itemID': '1',
        'location': 'Vancouver',
        'timestamp': 123456789,
        'borrowerID': 'user1'
    }
    table = items_table
    table.put_item(Item=item)
    event = {
        'body': '{"itemID": "1"}'
    }
    response = handler(event, None)
    assert response['statusCode'] == 200
    assert json.loads(response['body'])['Attributes']['borrowerID'] == None


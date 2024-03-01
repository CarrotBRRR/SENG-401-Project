import pytest
from main import *
from moto import mock_aws
import boto3

def test_parse_event_body_with_dict():
    event_body = {"key": "value"}
    assert parse_event_body(event_body) == event_body, "Should return the original dictionary without changes."

def test_parse_event_body_with_json_string():
    event_body = '{"key": "value"}'
    expected_result = {"key": "value"}
    assert parse_event_body(event_body) == expected_result, "Should convert JSON string to dictionary."

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

def test_append_borrower_to_borrow_requests(items_table):
    items_table.put_item(
        Item={
            'itemID': '1',
            'borrowRequests': [],
            'timestamp': 123,
            'location': 'Toronto'
        }
    )
    
    append_borrower_to_borrow_requests(items_table, '1', 'AGJKL')
    response = items_table.get_item(Key={'itemID': '1'})
    assert response['Item']['borrowRequests'] == ['AGJKL'], "Should append a borrowerID to the borrowRequests array."

def test_handler_success(items_table):
    items_table.put_item(
        Item={
            'itemID': '1',
            'borrowRequests': ["JX152"],
            'timestamp': 123,
            'location': 'Toronto'
        }
    )
    event = {
        "body": '{"itemID": "1", "borrowerID": "AGJKL"}'
    }
    context = None
    response = handler(event, context)
    assert response['statusCode'] == 200, "Should return a 200 status code."
    assert json.loads(response['body'])['updatedAttributes']['borrowRequests'] == ['JX152','AGJKL'], "Should append a borrowerID to the borrowRequests array."
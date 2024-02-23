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
        yield

@pytest.fixture
def dynamodb_table(dynamodb_mock):
    """Create a mock DynamoDB table."""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    dynamodb.create_table(
        TableName='items-30144999',
        KeySchema=[{'AttributeName': 'itemID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'itemID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )
    return dynamodb.Table('items-30144999')

def test_parse_event_body_with_dict():
    event_body = {"key": "value"}
    assert parse_event_body(event_body) == event_body

def test_parse_event_body_with_json_string():
    event_body = '{"key": "value"}'
    expected_result = {"key": "value"}
    assert parse_event_body(event_body) == expected_result

def test_remove_borrowerID_from_item(dynamodb_table):
    # Prepopulate the table with an item
    itemID = '1'
    dynamodb_table.put_item(Item={'itemID': itemID, 'borrowerID': '12345'})

    # Perform the remove operation
    update_borrowerID_to_null_in_item(dynamodb_table, itemID)

    # Fetch the updated item
    response = dynamodb_table.get_item(Key={'itemID': itemID})
    assert 'Item' in response
    item = response['Item']
    # Assert that the borrowerID is now null for itemID 1
    assert item['borrowerID'] is None



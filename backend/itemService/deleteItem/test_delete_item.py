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


def test_remove_item(dynamodb_mock):
    table_name = 'items-30144999'
    dynamodb_mock.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'itemID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'itemID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    table = dynamodb_mock.Table(table_name)
    itemID = 'testID'
    table.put_item(Item={'itemID': itemID})

    assert 'Item' in table.get_item(Key={'itemID': itemID})

    remove_item(table, itemID)

    resp = table.get_item(Key={'itemID': itemID})
    assert 'Item' not in resp


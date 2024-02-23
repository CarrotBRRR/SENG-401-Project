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
        KeySchema=[{'AttributeName': 'itemID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'itemID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )
    return table

def test_fetch_items_from_timestamp(dynamodb_mock, items_table):
    """Test the fetch_items_from_timestamp function."""
    items_table.put_item(Item={'itemID': '1', 'timestamp': 1613544690})
    items_table.put_item(Item={'itemID': '2', 'timestamp': 1613544691})
    items_table.put_item(Item={'itemID': '3', 'timestamp': 1613544692})

    items = fetch_items_from_timestamp('items-30144999', 1613544691, 2)
    assert len(items) == 1
    assert items[0]['itemID'] == '1'
    assert items[0]['timestamp'] == 1613544690

def test_handler(dynamodb_mock, items_table):
    """Test the handler function."""
    items_table.put_item(Item={'itemID': '1', 'timestamp': 1613544690})
    items_table.put_item(Item={'itemID': '2', 'timestamp': 1613544691})
    items_table.put_item(Item={'itemID': '3', 'timestamp': 1613544692})

    event = {
        "headers": {
            "startTimestamp": "1613544691",
            "pageCount": "2"
        }
    }
    response = handler(event, {})
    body = json.loads(response['body'])
    items = body['items']
    assert response['statusCode'] == 200
    assert len(items) == 1
    assert items[0]['itemID'] == '1'
    assert items[0]['timestamp'] == 1613544690
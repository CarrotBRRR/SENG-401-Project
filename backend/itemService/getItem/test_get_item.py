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

def test_parse_event_body():
    assert parse_event_body('{"key": "value"}') == {"key": "value"}
    assert parse_event_body({"key": "value"}) == {"key": "value"}


def test_fetch_items_after_itemID_no_lastItemID(items_table):
    items_table.put_item(Item={'itemID': '1'})
    items_table.put_item(Item={'itemID': '2'})
    items = fetch_items_after_itemID('items-30144999', '', 1)
    assert len(items) == 1


def test_handler_with_lastItemID(dynamodb_mock, items_table):
    items_table.put_item(Item={'itemID': '1'})
    items_table.put_item(Item={'itemID': '2'})
    event = {
        'body': json.dumps({'lastItemID': '1', 'pagecount': 1})
    }
    response = handler(event, None)
    assert response['statusCode'] == 200
    items = json.loads(response['body'])['items']
    assert len(items) == 1
    assert items[0]['itemID'] == '2'

def test_handler_no_lastItemID(dynamodb_mock, items_table):
    items_table.put_item(Item={'itemID': '1'})
    items_table.put_item(Item={'itemID': '2'})
    event = {
        'body': json.dumps({'pagecount': 2})
    }
    response = handler(event, None)
    assert response['statusCode'] == 200
    print(response)
    items = json.loads(response['body'])['items']
    assert len(items) == 2


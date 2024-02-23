import pytest
from main import *
from moto import mock_aws
import boto3
import os

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

@pytest.fixture
def dynamodb_mock(aws_credentials):
    with mock_aws():
        yield boto3.resource('dynamodb', region_name='ca-central-1')

def test_insert_item_in_table(dynamodb_mock):
    table_name = 'items-30144999'
    dynamodb_mock.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'itemID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'itemID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    table = dynamodb_mock.Table(table_name)

    mock_item = {
        'lenderID': "Len Derr",
        'itemName': "Eye Temm",
        'itemID': '69420',
        'description': "a description",
        'maxBorrowDays': 69,
        'image': ["url.com", 'anotherurl.com'],
        'imageHash': ["HAHAHASH", "anotherHAHAsh"]
    }

    insertion = insert_item_in_table(table, mock_item)

    response = table.get_item(Key={'itemID': '69420'})

    assert insertion['ResponseMetadata']['HTTPStatusCode'] == 200

    assert 'Item' in response
    assert response['Item']['itemID'] == '69420'
    assert response['Item']['lenderID'] == 'Len Derr'
    assert response['Item']['itemName'] == 'Eye Temm'
    assert response['Item']['description'] == 'a description'
    assert response['Item']['maxBorrowDays'] == 69
    assert response['Item']['image'] == ["url.com", 'anotherurl.com']
    assert response['Item']['imageHash'] == ["HAHAHASH", "anotherHAHAsh"]


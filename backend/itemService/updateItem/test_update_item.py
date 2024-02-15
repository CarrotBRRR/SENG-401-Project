from moto import mock_aws
from main import *
import os
import pytest

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

def test_edit_item_in_table(dynamodb_mock):
    table_name = 'items-30144999'
    dynamodb_mock.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'itemID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'itemID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    table = dynamodb_mock.Table(table_name)

    mock_item = {
        'lenderID': 'Len Derr',
        'itemName': 'Eye Temm',
        'itemID': '69420',
        'description': 'a description',
        'maxBorrowDays': 69,
        'image': 'url.com',
        'imageHash': 'HAHAHASH'
    }

    table.put_item(Item=mock_item)

    setup_item = table.get_item(Key={'itemID': '69420'})

    assert setup_item['Item']['itemName'] == "Eye Temm"

    mock_update = {
        'itemID': '69420',
        'itemName': 'aight \'em',
        'lenderID': 'Len Derr',
        'description': 'a new description',
        'maxBorrowDays': 420,
        'image': 'url2.com',
        'imageHash': 'hashbrown'
    }

    update = update_item_in_table(table, mock_update)

    assert update['ResponseMetadata']['HTTPStatusCode'] == 200

    response = table.get_item(Key={'itemID': '69420'})

    assert response['Item']['itemName'] == "aight \'em"
    assert response['Item']['description'] == "a new description"
    assert response['Item']['maxBorrowDays'] == 420
    assert response['Item']['image'] == "url2.com"
    assert response['Item']['imageHash'] == "hashbrown"

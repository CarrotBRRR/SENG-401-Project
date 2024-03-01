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
        'condition': 'Used - New',
        'tags': 'tag1, tag2',
        'location': 'a location',
        'description': 'a description',
        'images': 'url.com',
        'imageHashes': 'HAHAHASH',
        'timestamp': '1234567890',
        'borrowerID': None
    }

    table.put_item(Item=mock_item)

    setup_item = table.get_item(Key={'itemID': '69420'})

    assert setup_item['Item']['itemName'] == "Eye Temm"
    assert setup_item['Item']['timestamp'] == "1234567890"
    
    mock_update = {
        'itemID': '69420',
        'itemName': 'aight \'em',
        'condition': 'Used - Good',
        'lenderID': 'Len Derr',
        'tags': 'tag3, tag4',
        'location': 'another location',
        'description': 'a new description',
        'images': ['url2.com', 'url3.com'],
        'imageHashes': ['hashbrown', 'otherthing'],
        'timestamp': '1234567890',
        'borrowerID': None
    }

    update = update_item_in_table(table, mock_update)

    assert update['ResponseMetadata']['HTTPStatusCode'] == 200

    response = table.get_item(Key={'itemID': '69420'})

    assert response['Item']['itemName'] == "aight \'em"
    assert response['Item']['description'] == "a new description"
    assert response['Item']['images'] == ['url2.com', 'url3.com']
    assert response['Item']['imageHashes'] == ['hashbrown', 'otherthing']
    assert response['Item']['condition'] == "Used - Good"
    assert response['Item']['tags'] == "tag3, tag4"
    assert response['Item']['location'] == "another location"
    assert response['Item']['timestamp'] == "1234567890"
    assert response['Item']['borrowerID'] == None

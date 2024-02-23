import pytest
from main import *
from moto import mock_aws
import boto3


# Mock AWS credentials
@pytest.fixture
def aws_credentials():
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

# Mock DynamoDB
@pytest.fixture
def dynamodb_mock(aws_credentials):
    with mock_aws():
        yield boto3.resource('dynamodb', region_name='ca-central-1')

def test_remove_item(dynamodb_mock):
    # Create a dummy table
    table_name = 'users-30144999'
    dynamodb_mock.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'userID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'userID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    # Insert dummy user
    table = dynamodb_mock.Table(table_name)
    userID = 'testID'
    table.put_item(Item={'userID': userID})

    # assert dummy user is in table
    assert 'Item' in table.get_item(Key={'userID': userID})
    
    # Delete dummy user and assert that its not there
    delete_account(table, userID)
    response = table.get_item(Key={'userID': userID})
    assert 'Item' not in response
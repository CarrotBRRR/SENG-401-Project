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

def test_update_account(dynamodb_mock):
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
    
    mock_user = {
        'userID': '123456',
        'name': 'John Doe',
        'rating': 4,
        'email': 'johndoe@testmail.com', 
        'bio': 'John Doe is a guy whose name is John Doe',
        'location': 'Calgary',
        'profilePicture': 'test.com',
        'imageHash': 'HASHMAP'
    }
    
    table.put_item(Item=mock_user)
    
    # assert dummy was successfully added
    assert_user = table.get_item(Key={'userID': '123456'})
    assert assert_user['Item']['name'] == 'John Doe'
    assert assert_user['Item']['rating'] == 4
    
    # update the old user
    mock_updated_user = {
        'userID': '123456',
        'name': 'Donald Duck',
        'rating': 5,
        'email': 'donaldduck@testmail.com', 
        'bio': 'Donald Duck is a guy whose name is not John Doe',
        'location': 'Calgary',
        'profilePicture': 'test.com',
        'imageHash': 'HASHMAP'
    }
    
    userID = '123456'
    response = update_account(table, userID, mock_user, mock_updated_user)
    
    # assert updated user
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    
    
    assert_updated_user = table.get_item(Key={'userID': '123456'})
    
    assert assert_updated_user['Item']['name'] ==  'Donald Duck'
    assert assert_updated_user['Item']['rating'] == 5
    assert assert_updated_user['Item']['email'] == 'donaldduck@testmail.com'
    assert assert_updated_user['Item']['bio'] == 'Donald Duck is a guy whose name is not John Doe'
    assert assert_updated_user['Item']['location'] == 'Calgary'
    assert assert_updated_user['Item']['profilePicture'] == 'test.com'
    assert assert_updated_user['Item']['imageHash'] == 'HASHMAP'
from main import *
import pytest
from moto import mock_aws
import boto3

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

def test_write_user_into_table(dynamodb_mock):
    "Tests writing to DynamoDB table with valid input"
    table_name = 'users-30144999'
    dynamodb_mock.create_table(
        TableName = table_name, 
        KeySchema = [{'AttributeName': 'userID', 'KeyType': 'HASH'}],
        AttributeDefinitions = [
            {'AttributeName': 'userID', 'AttributeType': 'S'},
            {'AttributeName': 'email', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[{
            'IndexName': 'EmailIndex',
            'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
            'Projection': {'ProjectionType': 'ALL'},
            'ProvisionedThroughput': {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        }],     
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    table = dynamodb_mock.Table(table_name)

    event = {"body": json.dumps({
        "name": "John Doe",
        "email": "john@example.com",
        "rating": 5,
        "bio": "Sample bio",
        "location": "Sample location"
    })}
    context = {}
    response = handler(event, context, table)

    assert response["statusCode"] == 200, "Status code should be 200 for successful execution"
    
    inserted_userID = json.loads(response["body"])["userID"]
    response = table.get_item(Key={'userID': inserted_userID})
    item_in_table = response.get('Item', {})

    inserted_item = json.loads(event['body'])
    for key, value in inserted_item.items():
        assert item_in_table.get(key) == value, f"Value for key {key} does not match in the DynamoDB table"

def test_existing_email(dynamodb_mock):
    "Tests handling existing email scenario"
    table_name = 'users-30144999'
    dynamodb_mock.create_table(
        TableName = table_name, 
        KeySchema = [{'AttributeName': 'userID', 'KeyType': 'HASH'}],
        AttributeDefinitions = [
            {'AttributeName': 'userID', 'AttributeType': 'S'},
            {'AttributeName': 'email', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[{
            'IndexName': 'EmailIndex',
            'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
            'Projection': {'ProjectionType': 'ALL'},
            'ProvisionedThroughput': {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        }],     
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    table = dynamodb_mock.Table(table_name)
    event = {"body": json.dumps({
        "userID": str(uuid.uuid4()),
        "name": "John Doe",
        "email": "john@example.com",
        "rating": 5,
        "bio": "Sample bio",
        "location": "Sample location"
    })}
    context = {}

    # Insert an item with the same email first
    table.put_item(Item=json.loads(event['body']))

    response = handler(event, context, table)

    assert response["statusCode"] == 400, "Status code should be 400 for existing email"
    assert "Email already exists" in response["body"], "Response body should contain 'Email already exists' message"

def test_missing_field():
    "Tests handling missing field scenario"
    event = {
        "body": json.dumps({
            "name": "John Doe",
            "rating": 4.5,
            "bio": "Test bio",
            "location": "Test location"
        })
    }
    context = {}

    response = handler(event, context)

    assert response["statusCode"] == 400, "Status code should be 400 for missing field"
    assert '{"message": "Missing required field: \'email\'"}' in response["body"], "Response body should contain 'Missing required field: email' message"
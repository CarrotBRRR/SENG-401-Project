from main import *
import pytest
from moto import mock_aws
import boto3
import uuid


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

def test_get_user_with_userID(dynamodb_mock):
    "Tests getting from DynamoDB table with valid input"
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
    userID = str(uuid.uuid4())
    table.put_item(
        Item={
            "userID": userID,
            "name": "John Doe",
            "email": "john@example.com",
            "rating": 5,
            "bio": "Sample bio",
            "location": "Sample location"
        }
    )
    headers = {
        "userid": userID,
    }
    event = {"headers": headers}
    context = {}
    response = handler(event, context, table)
    print(response)

    assert response["statusCode"] == 200, "Status code should be 200 for successful execution."
    response_body = json.loads(response['body'])
    assert response_body["userID"] == userID, "Incorrect userID returned"
    assert response_body["name"] == "John Doe", "Incorrect name returned"
    assert response_body["email"] == "john@example.com", "Incorrect email returned"
    assert response_body["rating"] == 5, "Incorrect rating returned"
    assert response_body["bio"] == "Sample bio", "Incorrect bio returned"
    assert response_body["location"] == "Sample location", "Incorrect location returned"

def test_get_user_with_email(dynamodb_mock):
    "Tests getting from DynamoDB table with valid input"
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
    userID = str(uuid.uuid4())
    table.put_item(
        Item={
            "userID": userID,
            "name": "John Doe",
            "email": "john@example.com",
            "rating": 5,
            "bio": "Sample bio",
            "location": "Sample location"
        }
    )
    headers = {
        "email": "john@example.com"
    }
    event = {"headers": headers}
    context = {}
    response = handler(event, context, table)

    assert response["statusCode"] == 200, "Status code should be 200 for successful execution."
    response_body = json.loads(response['body'])
    assert response_body["userID"] == userID, "Incorrect userID returned"
    assert response_body["name"] == "John Doe", "Incorrect name returned"
    assert response_body["email"] == "john@example.com", "Incorrect email returned"
    assert response_body["rating"] == 5, "Incorrect rating returned"
    assert response_body["bio"] == "Sample bio", "Incorrect bio returned"
    assert response_body["location"] == "Sample location", "Incorrect location returned"

def test_missing_user_id_and_email(dynamodb_mock):
    "Tests when both userID and email are missing from the request"
    table_name = 'users-30144999'
    dynamodb_mock.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'userID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[
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
    headers = {}
    event = {"headers": headers}
    context = {}
    response = handler(event, context, table)

    assert response["statusCode"] == 400, "Status code should be 400 for missing userID and email"
    response_body = json.loads(response['body'])
    assert response_body["message"] == "Missing userID or email in request", "Incorrect error message returned"

def test_user_not_found(dynamodb_mock):
    "Tests when the user is not found in the DynamoDB table"
    table_name = 'users-30144999'
    dynamodb_mock.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'userID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[
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
    headers = {"userID": str(uuid.uuid4()), "email": "test@example.com"}
    event = {"headers": headers}
    context = {}
    response = handler(event, context, table)

    assert response["statusCode"] == 404, "Status code should be 404 for user not found"
    response_body = json.loads(response['body'])
    assert response_body["message"] == "User not found", "Incorrect error message returned"

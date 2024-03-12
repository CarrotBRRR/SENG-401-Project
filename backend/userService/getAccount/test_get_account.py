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

def test_get_user_from_table(dynamodb_mock):
    "Tests getting from DynamoDB table with valid input"
    table_name = 'users-30144999'
    dynamodb_mock.create_table(
        TableName = table_name, 
        KeySchema = [{'AttributeName': 'userID', 'KeyType': 'HASH'}],
        AttributeDefinitions = [{'AttributeName': 'userID', 'AttributeType': 'S'}],     
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
    event = {"body": json.dumps({"userID": userID})}
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
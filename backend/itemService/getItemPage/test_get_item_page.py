import pytest
from moto import mock_aws
import boto3
import json
from main import *
import random

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
        KeySchema=[
            {'AttributeName': 'itemID', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'location', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'N'},
            {'AttributeName': 'itemID', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'LocationTimestampIndex',
                'KeySchema': [
                    {'AttributeName': 'location', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'} 
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            }
        ]
    )
    return table

def test_parse_event_body():
    assert parse_event_body('{"key": "value"}') == {"key": "value"}
    assert parse_event_body({"key": "value"}) == {"key": "value"}




def populate_table_with_items(table):
    """Helper function to populate table with a mix of items."""
    items = [
        {'itemID': '1', 'location': 'loc1', 'timestamp': 123, 'borrowerID': 'borrower1'},
        {'itemID': '2', 'location': 'loc1', 'timestamp': 124},  # No borrowerID
        {'itemID': '3', 'location': 'loc1', 'timestamp': 125, 'borrowerID': 'borrower2'},
        {'itemID': '4', 'location': 'loc1', 'timestamp': 126},  # No borrowerID
        {'itemID': '5', 'location': 'loc1', 'timestamp': 127}   # No borrowerID
    ]
    for item in items:
        table.put_item(Item=item)

def test_pagination_with_exact_page_size(items_table):
    """Test fetching items where the number of items exactly matches the page size."""
    populate_table_with_items(items_table)
    # Assuming populate_table_with_items adds 3 items without borrowerID
    fetched_items, last_evaluated_key = fetch_items_without_borrowerID_with_pagination(
        'items-30144999', 'loc1', None, 3
    )
    assert len(fetched_items) == 3, "Should fetch exactly 3 items"
    assert last_evaluated_key is None, "There should not be a next page"

def test_pagination_with_additional_queries_needed(items_table):
    """Test fetching items where additional queries are needed due to filtered items."""
    populate_table_with_items(items_table)
    # Request 2 items, but since items with borrowerID are skipped, it might need more queries
    fetched_items, last_evaluated_key = fetch_items_without_borrowerID_with_pagination(
        'items-30144999', 'loc1', None, 2
    )
    assert len(fetched_items) == 2, "Should fetch exactly 2 items"
    assert last_evaluated_key is not None, "There should be more items available"

def test_pagination_last_page_with_fewer_items(items_table):
    """Test fetching the last page of items when there are fewer items than the page size."""
    populate_table_with_items(items_table)
    # First, fetch 2 items to simulate partial consumption
    _, last_evaluated_key = fetch_items_without_borrowerID_with_pagination(
        'items-30144999', 'loc1', None, 2
    )
    # Now, fetch with the last_evaluated_key to get the last page
    fetched_items, last_evaluated_key_next = fetch_items_without_borrowerID_with_pagination(
        'items-30144999', 'loc1', last_evaluated_key, 2
    )
    # Assuming there was 1 item left without borrowerID
    assert len(fetched_items) == 1, "Should fetch exactly 1 remaining item"
    assert last_evaluated_key_next is None, "There should not be more items available"

def test_pagination_with_no_matching_items(items_table):
    """Test fetching items when none match the filter criteria."""
    populate_table_with_items(items_table)
    # Fetch with a location that doesn't match any items
    fetched_items, last_evaluated_key = fetch_items_without_borrowerID_with_pagination(
        'items-30144999', 'loc2', None, 3  # Assuming 'loc2' items don't exist
    )
    assert len(fetched_items) == 0, "Should not fetch any items"
    assert last_evaluated_key is None, "There should not be a next page"

def populate_large_table(table, num_items, num_borrowed_items):
    """Helper function to populate table with a large number of items. Some items are borrowed at random indices."""
    # Populate a set of num_borrowed_items that are less than num_items
    borrowed_indices = random.sample(range(num_items), num_borrowed_items)
    print(borrowed_indices)
    for i in range(num_items):
        item = {
            'itemID': str(i),
            'location': 'loc1',
            'timestamp': i,
            'itemName': 'item' + str(i),
            'description': 'description' + str(i),
        }
        if i in borrowed_indices:
            item['borrowerID'] = 'borrower' + str(i)
        table.put_item(Item=item)

def test_pagination_without_duplicates(items_table):
    """Test fetching multiple pages without duplicating items across pages."""
    populate_large_table(items_table, 21, 10)

    # Fetch the first page with 10 items
    first_page_items, last_evaluated_key = fetch_items_without_borrowerID_with_pagination(
        'items-30144999', 'loc1', None, 10
    )
    assert len(first_page_items) == 10, "First page should contain exactly 10 items"

    # Use the LastEvaluatedKey to fetch the next page
    second_page_items, _ = fetch_items_without_borrowerID_with_pagination(
        'items-30144999', 'loc1', last_evaluated_key, 10
    )
    assert len(second_page_items) == 1, "Second page should contain 1 item"

    # Verify no duplicates between first page and second page
    first_page_ids = {item['itemID'] for item in first_page_items}
    second_page_ids = {item['itemID'] for item in second_page_items}
    assert first_page_ids.isdisjoint(second_page_ids), "No item should appear on both the first and second pages"

def test_pagination_with_search(items_table):
    """Test fetching items with a search query."""
    items_table.put_item(
        Item={
            'itemID': '1',
            'location': 'loc1',
            'timestamp': 123,
            'itemName': 'Used hammer',
            'description': 'the thing is great'
        }
    )
    items_table.put_item(
        Item={
            'itemID': '2',
            'location': 'loc1',
            'timestamp': 124,
            'itemName': 'New thing',
            'description': 'the hammer is great'
        }
    )
    items_table.put_item(
        Item={
            'itemID': '3',
            'location': 'loc1',
            'timestamp': 125,
            'itemName': 'Used thing',
            'description': 'the thing is great'
        }
    )

    # Fetch items with a search query
    fetched_items, _ = fetch_items_without_borrowerID_with_pagination(
        'items-30144999', 'loc1', None, 10, 'hammer'
    )
    assert len(fetched_items) == 2, "Should fetch exactly 2 items"
    assert fetched_items[0]['itemName'] == 'New thing', "Should fetch the correct items"
    assert fetched_items[1]['itemName'] == 'Used hammer', "Should fetch the correct items"


# test fetch_items_without_borrowerID_with_pagination with search = None and category = Adventure
def test_pagination_with_category(items_table):
    """Test fetching items with a category query."""
    items_table.put_item(
        Item={
            'itemID': '1',
            'location': 'loc1',
            'timestamp': 123,
            'itemName': 'item1',
            'description': 'description1',
            'category': 'Adventure'
        }
    )
    items_table.put_item(
        Item={
            'itemID': '2',
            'location': 'loc1',
            'timestamp': 124,
            'itemName': 'item2',
            'description': 'description2',
            'category': 'Adventure'
        }
    )
    items_table.put_item(
        Item={
            'itemID': '3',
            'location': 'loc1',
            'timestamp': 125,
            'itemName': 'item3',
            'description': 'description3',
            'category': 'Adventure'
        },
   )
    items_table.put_item(
        Item={
            'itemID': '4',
            'location': 'loc1',
            'timestamp': 126,
            'itemName': 'item4',
            'description': 'description4',
            'category': 'Adult'
        }
    )

    # Fetch items with a category query
    fetched_items, _ = fetch_items_without_borrowerID_with_pagination(
        'items-30144999', 'loc1', None, 10, None, 'Adventure'
    )
    assert len(fetched_items) == 3, "Should fetch exactly 3 items"
    assert fetched_items[0]['itemName'] == 'item3', "Should fetch the correct items"
    assert fetched_items[1]['itemName'] == 'item2', "Should fetch the correct items"
    assert fetched_items[2]['itemName'] == 'item1', "Should fetch the correct items"

def test_handler_with_valid_location_and_pagecount(items_table):
    """Test handler with valid location and pagecount."""
    populate_large_table(items_table, 30, 20)
    event = {
        "headers": {
            "location": "loc1",
            "pagecount": "5"
        }
    }

    response = handler(event, None)
    body = json.loads(response['body'])
    items = body['items']
    last_evaluated_key = body['last_evaluated_key']
    assert response['statusCode'] == 200, "Should return a 200 status code"
    assert len(items) == 5, "Should return 5 items"
    assert last_evaluated_key is not None, "Should return a last_evaluated_key"

    event = {
        "headers": {
            "location": "loc1",
            "pagecount": "5",
            "lastitem": json.dumps(last_evaluated_key)
        }
    }
    response = handler(event, None)
    body = json.loads(response['body'])
    items = body['items']
    last_evaluated_key = body['last_evaluated_key']
    assert response['statusCode'] == 200, "Should return a 200 status code"
    assert len(items) == 5, "Should return 5 items"


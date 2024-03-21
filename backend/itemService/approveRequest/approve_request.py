import boto3
import json
from decimal import Decimal

def get_dynamodb_table(table_name):
    """Initialize a DynamoDB resource and get the table."""
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
    table = dynamodb.Table(table_name)
    return table

def decimal_default(obj):
    """Convert Decimal objects to float. Can be passed as the 'default' parameter to json.dumps()."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def parse_event_body(event_body):
    """Parse the event body, converting from JSON string to dictionary if necessary."""
    if isinstance(event_body, str):
        return json.loads(event_body)
    return event_body

def set_borrow_requests_in_table(table, itemID, requests):
    """Update an item in the DynamoDB table."""
    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="set borrowRequests = :b",
        ExpressionAttributeValues={
            ':b': requests
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def remove_borrower_id_from_borrow_requests(table, itemID, borrowerID_index):
    """Remove a borrowerID from the borrowRequests array in the DynamoDB table."""
    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="REMOVE borrowRequests[{}]"
        .format(borrowerID_index),
        ReturnValues="UPDATED_NEW"
    )
    return response

def handler(event, context):
    try:
        table_name = 'items-30144999'
        table = get_dynamodb_table(table_name)
        body = parse_event_body(event["body"])
        itemID = body["itemID"]
        borrowerID = body["borrowerID"]
        
        item = table.get_item(Key={'itemID': itemID})
        borrow_requests = item.get('Item', {}).get('borrowRequests', [])

        # Find the index of the borrowerID in the borrowRequests array
        borrowerID_index = next((i for i, d in enumerate(borrow_requests) if d["borrowerID"] == borrowerID), None)
        if borrowerID_index is None:
            raise ValueError("Borrower ID not found in borrow requests")
        
        # create a new borrow request with the same start and end dates, but with status "approved"
        data = {
            "borrowerID": borrowerID,
            "startDate": borrow_requests[borrowerID_index]["startDate"],
            "endDate": borrow_requests[borrowerID_index]["endDate"],
            "status": "approved"
        }

        responses = []
        # remove the borrowerID from the borrowRequests array
        responses.append(remove_borrower_id_from_borrow_requests(table, itemID, borrowerID_index))
        # set the borrowRequests array to the new borrow request
        responses.append(set_borrow_requests_in_table(table, itemID, borrow_requests))
        
        return {
            'statusCode': 200,
            'body': json.dumps(responses, default=decimal_default)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }
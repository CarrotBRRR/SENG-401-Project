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

def update_start_end_dates_in_table(table, itemID, startDate, endDate):
    """Update the start and end dates in the DynamoDB table."""
    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="set startDate = :s, endDate = :e",
        ExpressionAttributeValues={
            ':s': startDate,
            ':e': endDate
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

def update_current_borrower_in_table(table, itemID, borrowerID):
    """Update the current borrower in the DynamoDB table."""
    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="set borrowerID = :b",
        ExpressionAttributeValues={
            ':b': borrowerID
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

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

def handler(event, context):
    try:
        table_name = 'items-30144999'
        table = get_dynamodb_table(table_name)
        body = parse_event_body(event["body"])
        itemID = body["itemID"]
        borrowerID = body["borrowerID"]
        
        current_item = table.get_item(
            Key={'itemID': itemID}
        )

        borrow_requests = current_item['Item']['borrowRequests']

        borrowerID_index = next((i for i, d in enumerate(borrow_requests) if d["borrowerID"] == borrowerID), None)
        if borrowerID_index is None:
            raise ValueError("Borrower ID not found in borrow requests")
        
        request = borrow_requests[borrowerID_index]

        startDate = Decimal(request['startDate'])
        endDate = Decimal(request['endDate'])

        new_request = {
            'borrowerID': borrowerID,
            'startDate': startDate,
            'endDate': endDate,
            'status': 'active'
        }

        responses = []

        # remove original request from borrowRequests
        responses.append(remove_borrower_id_from_borrow_requests(table, itemID, borrowerID_index))

        # retrieve item again to get updated borrowRequests
        item_removed_request = table.get_item(
            Key={'itemID': itemID}
        )

        # append updated request to borrowRequests
        requests = item_removed_request['Item']['borrowRequests']
        requests.append(new_request)

        # update borrowRequests, startDate, endDate, and borrowerID
        responses.append(set_borrow_requests_in_table(table, itemID, requests))
        responses.append(update_start_end_dates_in_table(table, itemID, startDate, endDate))
        responses.append(update_current_borrower_in_table(table, itemID, borrowerID))

        return {
            'statusCode': 200,
            'body': json.dumps(responses, default=decimal_default)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

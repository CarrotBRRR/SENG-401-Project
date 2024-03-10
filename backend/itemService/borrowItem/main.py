import boto3
import json

def get_dynamodb_table(table_name):
    """Initialize a DynamoDB resource and get the table."""
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
    table = dynamodb.Table(table_name)
    return table

def parse_event_body(event_body):
    """Parse the event body, converting from JSON string to dictionary if necessary."""
    if isinstance(event_body, str):
        return json.loads(event_body)
    return event_body

def update_item_in_table(table, itemID, borrowerID):
    """Update an item in the DynamoDB table."""
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
        
        current_item = table.get_item(
            Key={'itemID': itemID}
        )
        if 'Item' not in current_item or 'borrowRequests' not in current_item['Item']:
            raise ValueError("Item or borrowRequests not found")

        borrow_requests = current_item['Item']['borrowRequests']
        if borrowerID in borrow_requests:
            borrowerID_index = borrow_requests.index(borrowerID)
            response = remove_borrower_id_from_borrow_requests(table, itemID, borrowerID_index)
        else:
            raise ValueError("borrowerID not found in borrowRequests")
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
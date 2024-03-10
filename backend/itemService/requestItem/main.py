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

def append_borrower_to_borrow_requests(table, itemID, borrowerID):
    """Append a borrowerID to the borrowRequests array in the DynamoDB table."""
    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="SET borrowRequests = list_append(if_not_exists(borrowRequests, :empty_list), :b)",
        ExpressionAttributeValues={
            ':b': [borrowerID],
            ':empty_list': []
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
        
        response = append_borrower_to_borrow_requests(table, itemID, borrowerID)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'BorrowerID appended successfully',
                'updatedAttributes': response['Attributes']
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

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

def update_borrowerID_to_null_in_item(table, itemID):
    """Set the borrowerID to null for an item in the DynamoDB table."""
    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="SET borrowerID = :val",
        ExpressionAttributeValues={
            ':val': None
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
        
        response = update_borrowerID_to_null_in_item(table, itemID)
        
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }


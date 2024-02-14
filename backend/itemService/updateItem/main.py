import boto3
import json

def get_dynamodb_table(table_name):
    """Initialize a DynamoDB resource and get the table."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return table

def parse_event_body(event_body):
    """Parse the event body, converting from JSON string to dictionary if necessary."""
    if isinstance(event_body, str):
        return json.loads(event_body)
    return event_body

# This is probably wrong?
def update_item_in_table(table, itemID, newInfo):
    """Update an item in the DynamoDB table."""
    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="set itemName = :S",
        ExpressionAttributeValues={
            ':S': newInfo["itemName"]
        },
        UpdateExpression="set description = :S",
        ExpressionAttributeValues={
            ':S': newInfo["description"]
        },
        UpdateExpression="set maxBorrowDays = :N",
        ExpressionAttributeValues={
            ':N': newInfo["maxBorrowDays"]
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
        itemName = body["name"]
        description = body["description"]
        maxBorrowDays = body["max_borrow_days"]

        newInfo = {
            'itemName': itemName,
            'description': description,
            'maxBorrowDays': maxBorrowDays
        }

        response = update_item_in_table(table, itemID, newInfo)
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }


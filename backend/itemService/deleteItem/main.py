
import boto3
import json

def get_dynamodb_table(table_name):
    """Initialize a DynamoDB resource and get the table."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return table


def remove_item(table, itemID):
    """Remove an item from the DynamoDB table."""
    response = table.delete_item(
        Key={
            'itemID': itemID
        }
    )
    return response

def handler(event, context):
    try:
        table_name = 'items-30144999'
        table = get_dynamodb_table(table_name)
        headers = event.get("headers", {})
        itemID = headers.get("itemID", {})
        
        response = remove_item(table, itemID)
        
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }



import boto3
import json
from decimal import Decimal

def get_dynamodb_table(table_name):
    """Initialize a DynamoDB resource and get the table."""
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
    table = dynamodb.Table(table_name)
    return table

def get_items_by_borrower_id(table, borrowerID, gsi_name):
    """Retrieve all items from the DynamoDB table for a given borrowerID using a GSI."""
    if borrowerID == '':
        return []
    response = table.query(
        IndexName=gsi_name,
        KeyConditionExpression='borrowerID = :borrowerID',
        ExpressionAttributeValues={
            ':borrowerID': borrowerID
        }
    )
    return response.get('Items', [])

def decimal_default(obj):
    """Convert Decimal objects to float. Can be passed as the 'default' parameter to json.dumps()."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def handler(event, context):
    try:
        table_name = 'items-30144999'
        gsi_name = 'BorrowerIDIndex'
        table = get_dynamodb_table(table_name)
        headers = event.get("headers", {})
        borrowerID = headers.get('borrowerid', '')
        if borrowerID == '':
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No borrowerID provided'
                })
            }
        items = get_items_by_borrower_id(table, borrowerID, gsi_name)
        
        items_converted = json.loads(json.dumps(items, default=decimal_default))

        return {
            'statusCode': 200,
            'body': json.dumps({
                'items': items_converted
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

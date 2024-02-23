import boto3
import json

def get_dynamodb_table(table_name):
    """Initialize a DynamoDB resource and get the table."""
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
    table = dynamodb.Table(table_name)
    return table


def fetch_items_from_timestamp(table_name, start_timestamp, pageCount):
    table = get_dynamodb_table(table_name)
    query_kwargs = {
        # Adjusted to query items with a timestamp less than the provided start_timestamp
        'KeyConditionExpression': '#ts < :start_ts',
        'ExpressionAttributeNames': {'#ts': 'timestamp'},
        'ExpressionAttributeValues': {':start_ts': {'N': str(start_timestamp)}},
        'Limit': pageCount,
        'ScanIndexForward': False  # Ensures items are fetched from newest to oldest
    }
    
    response = table.query(**query_kwargs)
    return response.get('Items', [])

def handler(event, context):
    try:
        headers = event.get("headers", {})
        
        # Ensure we convert the timestamp from the headers to a float, as it's provided as a string
        start_timestamp = headers.get('startTimestamp', '')
        if start_timestamp:
            start_timestamp = float(start_timestamp)
        
        pageCount = headers.get('pageCount', '10')
        pageCount = int(pageCount)
        table_name = 'items-30144999'
        
        items = fetch_items_from_timestamp(table_name, start_timestamp, pageCount)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'items': items})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

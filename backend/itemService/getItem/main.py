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

def fetch_items_after_itemID(table_name, last_itemID, pageCount):
    table = get_dynamodb_table(table_name)
    scan_kwargs = {
        'Limit': pageCount
    }

    if last_itemID != '':
        scan_kwargs['ExclusiveStartKey'] = {'itemID': last_itemID}
    
    response = table.scan(**scan_kwargs)
    return response.get('Items', [])

def handler(event, context):
    try:
        body = parse_event_body(event['body'])
        last_itemID = body.get('lastItemID', '')
        pageCount = int(body['pageCount'])  
        table_name = 'items-30144999'  
        
        items = fetch_items_after_itemID(table_name, last_itemID, pageCount)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'items': items})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

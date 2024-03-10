import boto3
import json
from decimal import Decimal

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

def decimal_default(obj):
    """Convert Decimal objects to float. Can be passed as the 'default' parameter to json.dumps()."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def fetch_items_without_borrowerID_with_pagination(table_name, location, exclusiveStartKey, pageCount, search=None, category=None):
    table = get_dynamodb_table(table_name)
    fetched_items = []
    last_evaluated_key = exclusiveStartKey or None

    # Start building the FilterExpression for attribute_not_exists condition
    filter_expressions = ['attribute_not_exists(borrowerID)']
    expression_attribute_values = {
        ':value': location,
    }
    expression_attribute_names = {}
    expression_attribute_names['#loc'] = 'location'

    # If search parameter is provided, add conditions for itemName and itemDescription
    if search:
        # Dynamically generate expression attribute names to avoid conflicts
        search_expression = "(contains(#itemName, :search) OR contains(#description, :search))"
        filter_expressions.append(search_expression)
        expression_attribute_values[':search'] = search
        expression_attribute_names['#itemName'] = 'itemName'
        expression_attribute_names['#description'] = 'description'
    
    if category:
        filter_expressions.append("(category = :category)")
        expression_attribute_values[':category'] = category
        expression_attribute_names['#category'] = 'category'


    while len(fetched_items) < pageCount:
        query_kwargs = {
            'IndexName': 'LocationTimestampIndex',
            'KeyConditionExpression': '#loc = :value',  # Updated to use alias
            'ExpressionAttributeValues': expression_attribute_values,
            'ExpressionAttributeNames': expression_attribute_names,  # Include this line
            'FilterExpression': " AND ".join(filter_expressions),
            'Limit': pageCount,
            'ScanIndexForward': False
        }
        
            
        if last_evaluated_key:
            query_kwargs['ExclusiveStartKey'] = last_evaluated_key

        response = table.query(**query_kwargs)
        fetched_items.extend(response.get('Items', []))

        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break  # No more items to fetch
    
    if len(fetched_items) > pageCount:
        last_evaluated_key = fetched_items[pageCount - 1]
    # If we fetched more items than needed due to the final query call, trim the list
    return fetched_items[:pageCount], last_evaluated_key




def handler(event, context):
    try:
        headers = event.get("headers", {})
        
        exclusiveStartKey = headers.get('lastitem', '')
        location = headers.get('location', '')
        pageCount = headers.get('pagecount', '10')
        pageCount = int(pageCount)
        search = headers.get('search')
        category = headers.get('category')
        table_name = 'items-30144999'
        if exclusiveStartKey != '':
            exclusiveStartKey = parse_event_body(exclusiveStartKey)
            exclusiveStartKey['timestamp'] = Decimal(str(exclusiveStartKey['timestamp']))
        
        items, last_evaluated_key = fetch_items_without_borrowerID_with_pagination(
            table_name, location, exclusiveStartKey, pageCount, search, category
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'items': items,
                'last_evaluated_key': last_evaluated_key
            }, default=decimal_default)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}, default=decimal_default)
        }

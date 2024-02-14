import boto3
import requests
import json
import uuid
import hashlib
import base64

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

def insert_item_in_table(table, itemID, data):
    """Insert an item into the DynamoDB table."""
    item = {
        'itemID': {'S': itemID},
        'lenderID': {'N': data['lenderID']},
        'itemName': {'S': data['itemName']},
        'description': {'S': data['description']},
        'maxBorrowDays': {'N': data['maxBorrowDays']},
        'imageURL': {'S': data['image']},
    }

    response = table.put_item(
        Key={
            'itemID': itemID
        },
        Item=item
    )
    return response

def post_image(image):
    # Get the credentials from AWS Parameter Store
    ssm = boto3.client('ssm')
    parameter_names = []
    key_string = ssm.get_parameter(
        Name="CloudinaryKey",
        WithDecryption=True
    )["Parameter"]["Value"]

    keys = key_string.split(",")

    cloud_name = keys[0]
    api_key = keys[1]
    api_secret = keys[2]

    url = f'https://api.cloudinary.com/v1_1/{cloud_name}/image/upload/'

    # Set up the payload
    payload = {
        'api_key': api_key,
    }
    file = {
        'file': image
    }
    payload["signature"] = create_signature(payload, api_secret)
    res = requests.post(url, files=file, data=payload)
    return res.json()

def create_signature(body, api_secret):
    exclude = ["api_key", "resource_type", "cloud_name"]
    sorted_body = sort_dict(body, exclude)
    query_string = create_query_string(sorted_body)
    query_string = f"{query_string}{api_secret}"
    hashed = hashlib.sha1(query_string.encode("utf-8")).hexdigest()
    return hashed

def sort_dict(dict, exclude):
    myKeys = list(dict.keys())
    myKeys.sort()
    for i in range(len(exclude)):
        if exclude[i] in myKeys:
            myKeys.remove(exclude[i])

    return {i: dict[i] for i in myKeys}

def create_query_string(dict):
    query_string = ""
    for ind, (key, value) in enumerate(dict.items()):
        query_string = f"{key}={value}" if ind == 0 else f"{query_string}&{key}={value}"
    return query_string

def handler(event, context):
    try:
        body = parse_event_body(event["body"])

        lenderID = body['lenderID']
        itemName = body['name']
        description = body['description']
        maxBorrowDays = body['max_borrow_days']

        # Create a unique item ID
        itemID = str(uuid.uuid4())

        # Get a timestamp for the item creation
        time = str(int(time.time()))

        raw_image = body['image']
        image_bytes = base64.b64decode(raw_image)
        filename = "./tmp/img.png"
        with open(filename, "wb") as f:
            f.write(image_bytes)

        image_url = post_image(filename)["secure_url"]

        data  = {
            'lenderID': lenderID,
            'itemName': itemName,
            'description': description,
            'maxBorrowDays': maxBorrowDays,
            'image': image_url,
            'timestamp': time
        }

        table_name = 'items-30144999'
        table = get_dynamodb_table(table_name)
        response = insert_item_in_table(table, itemID, data)

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

# test function
def add(a, b):
    return a + b

import boto3
import requests
import json
import hashlib
import base64
from decimal import Decimal

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

def update_item_in_table(table, newData):
    """Update an item in the DynamoDB table."""
    response = table.put_item(
        Item=newData,
        ReturnValues='ALL_OLD'
    )
    return response

def post_image(image, timestamp):
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

    # Set up the URL
    url = f'https://api.cloudinary.com/v1_1/{cloud_name}/image/upload/'

    # Set up the payload
    payload = {
        'api_key': api_key,
        'timestamp': timestamp
    }
    file = {
        'file': image
    }

    # Create a signature and add it to the payload
    payload["signature"] = create_signature(payload, api_secret)

    # Post the image to Cloudinary
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
        # Parse the event body
        body = parse_event_body(event["body"])
        itemID = body["itemID"]

        # Get the table and retrieve the old values
        table_name = 'items-30144999'
        table = get_dynamodb_table(table_name)
        item = table.get_item(Key={"itemID": itemID})["Item"]

        if item is None:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }

        timestamp = item["timestamp"]
        lenderID = item["lenderID"]

        # Get the new values
        itemName = body["listingTitle"]
        description = body["description"]
        condition = body["condition"]
        location = body["location"]
        category = body["category"]

        # Get the image and hashes
        raw_images = body["images"]
        image_urls = []
        for raw_image in raw_images:
            if raw_image is not None and raw_image != "null":
                image_bytes = base64.b64decode(raw_image)
                # If the image is not a Cloudinary link, upload it to Cloudinary, and update the image URL
                if not raw_image.startswith("https://res.cloudinary.com") and raw_image is not None:
                # Save the image to a temp file
                    filename = "/tmp/img.png"
                    stringtime = str(timestamp)
                    
                    with open(filename, "wb") as f:
                        f.write(image_bytes)

                    with open(filename, "rb") as f:
                        response = post_image(f, stringtime)

                    image_url = response["secure_url"]
                    
                # If the image has not changed, use the old image URL and hash
                else: 
                    image_url = raw_image

                image_urls.append(image_url)

        # Create a new item object
        newInfo = {
            'itemID': itemID,
            'itemName': itemName,
            'condition': condition,
            'description': description,
            'category': category,
            'location': location,
            'images': image_urls,
            'lenderID': lenderID,
            'timestamp': timestamp,
        }

        # Update the item in the table
        response = update_item_in_table(table, newInfo)
        return {
            'statusCode': 200,
            'body': json.dumps(response['ResponseMetadata'])
        }

    except Exception as e:

        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }


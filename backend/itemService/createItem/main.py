import boto3
import requests
import json
import uuid
import time
import hashlib
import base64

def handler(event, context):
    print(event)

    body = event['body']
    data = json.loads(body)

    lenderID = data['lenderID']
    itemName = data['name']
    description = data['description']
    maxBorrowDays = data['max_borrow_days']

    # Create a unique item ID
    itemID = str(uuid.uuid4())

    # Get a timestamp for the item creation
    time = str(int(time.time()))

    raw_image = data['image']
    image_bytes = base64.b64decode(raw_image)
    filename = "/tmp/img.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)

    image_url = post_image(filename)["secure_url"]

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

# test function
def add(a, b):
    return a + b

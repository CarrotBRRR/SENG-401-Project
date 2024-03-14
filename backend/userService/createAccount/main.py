import json
import boto3
import uuid
import traceback
import base64
import hashlib
from decimal import Decimal
import time
import requests

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

def create_signature(body, api_secret):
    exclude = ["api_key", "resource_type", "cloud_name"]
    sorted_body = sort_dict(body, exclude)
    query_string = create_query_string(sorted_body)
    query_string = f"{query_string}{api_secret}"
    hashed = hashlib.sha1(query_string.encode("utf-8")).hexdigest()
    return hashed

def post_to_cloudinary(file, timestamp):
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
        'file': file
    }

    # Create a signature and add it to the payload
    payload["signature"] = create_signature(payload, api_secret)

    # Post the image to Cloudinary
    res = requests.post(url, files=file, data=payload)
    print(res.json())
    return res.json()

def handler(event, context, table=None):
    # pass in table for testing
    if table is None:
        dynamodb_resource = boto3.resource("dynamodb", region_name='ca-central-1')
        table = dynamodb_resource.Table("users-30144999")  

    data = json.loads(event["body"])

    try:
        # check if email already exists
        response = table.query(
            IndexName='EmailIndex',  
            KeyConditionExpression=boto3.dynamodb.conditions.Key("email").eq(data["email"])
        )
        if response["Count"] > 0:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "Email already exists"
                })
            }
        # if email doesn't exist, create new user
        item={
            "userID": str(uuid.uuid4()),
            "name": data["name"],
            "email": data["email"],
            "rating": data["rating"],
            "bio": data["bio"],
            "location": data["location"]
            }
        # check if request contains profile pic
        if data.get("image") is not None and data.get("image") != "null": 
            profile_pic = data.get("image")
            item["profilePicture"] = profile_pic

            # decode image and hash it 
            image_bytes = base64.b64decode(profile_pic)
            image_hash = hashlib.sha256(image_bytes).hexdigest()

            item["imageHash"] = image_hash

            # Save the image to a temp file
            filename = "/tmp/img.png"

            with open(filename, "wb") as f:
                f.write(image_bytes)
            
            with open(filename, "rb") as f:
                post_to_cloudinary(f, Decimal(time.time()))

            
        table.put_item(Item=item)
        return {
            "statusCode": 200,
                "body": json.dumps(item)
        }
    except KeyError as ke:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"Missing required field: {str(ke)}"
            })
        }
    except Exception as e:
        print(f"Exception: {e}")
        traceback.print_exc()
        return {
            "statusCode": 500,
                "body": json.dumps({
                    "message": str(e),
                    "stack_trace": traceback.format_exc()
                })}
from boto3.dynamodb.conditions import Key
import json
import boto3
from decimal import Decimal


def handler(event, context, table=None):
    # pass in table for testing
    if table is None:
        dynamodb_resource = boto3.resource("dynamodb", region_name='ca-central-1')
        table = dynamodb_resource.Table("users-30144999")  
    
    data = json.loads(event["body"])
    
    # check if request contains userID or email
    if "userID" in data:
        key_condition = Key("userID").eq(data["userID"])
    elif "email" in data:
        key_condition = Key("email").eq(data["email"])
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Missing userID or email in request"
            })
        }
    
    try:
        res = table.query(KeyConditionExpression=key_condition)
        items = res["Items"]

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "User not found"
                })
            }
        
        # convert decimal to floats for JSON serialization
        for item in items:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)
        return {
            "statusCode": 200,
            "body": json.dumps(items)
        }
    except Exception as e:
        print(f"Exception: {e}")
        return {
            "statusCode": 500,
                "body": json.dumps({
                    "message": str(e)
                })     
        }
from boto3.dynamodb.conditions import Key
import json
import boto3
from decimal import Decimal


def handler(event, context, table=None):
    # pass in table for testing
    if table is None:
        dynamodb_resource = boto3.resource("dynamodb", region_name='ca-central-1')
        table = dynamodb_resource.Table("users-30144999")  
    
    headers = event["headers"]
    userID = headers.get('userID') 
    email = headers.get('email')
    
    # check if request contains userID or email

    if not userID and not email:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Missing userID or email in request"
            })
        }
    
    try:
        # use gsi for email if request contains email
        if email:
            res = table.query(
                IndexName='EmailIndex',
                KeyConditionExpression=Key("email").eq(email)
            )
        else:
            res = table.query(KeyConditionExpression=Key("userID").eq(userID))
        
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
        
        if len(items) == 1:
            return {
                "statusCode": 200,
                "body": json.dumps(items[0])
            }
        else:
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

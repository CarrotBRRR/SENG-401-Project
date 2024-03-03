from boto3.dynamodb.conditions import Key
import json
import boto3
from decimal import Decimal



def handler(event, context, table=None):
    if table is None:
        dynamodb_resource = boto3.resource("dynamodb", region_name='ca-central-1')
        table = dynamodb_resource.Table("users-30144999")  
    data = json.loads(event["body"])
    userID = data["userID"]
    try:
        res = table.query(KeyConditionExpression=Key("userID").eq(userID))
        items = res["Items"]
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

# Put email in headers:
# fetch('your-api-endpoint', {
#     method: 'GET',
#     headers: {
#         'Content-Type': 'application/json',
#         'email': email // Include email in headers
#     }
# })

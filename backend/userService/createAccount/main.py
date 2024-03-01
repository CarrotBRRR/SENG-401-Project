import json
import boto3
import uuid


def handler(event, context, table=None):
    # pass in table for testing
    if table is None:
        dynamodb_resource = boto3.resource("dynamodb", region_name='ca-central-1')
        table = dynamodb_resource.Table("users-30144999")  

    data = json.loads(event["body"])
    try:
        item={
            "userID": str(uuid.uuid4()),
            "name": data["name"],
            "email": data["email"],
            "rating": data["rating"],
            "bio": data["bio"],
            "location": data["location"]
            }
        table.put_item(Item=item)
        return {
            "statusCode": 200,
                "body": json.dumps(item)
        }
    except Exception as e:
        print(f"Exception: {e}")
        return {
            "statusCode": 500,
                "body": json.dumps({
                    "message": str(e)
                })}




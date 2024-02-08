import json
import boto3
import uuid

dynamodb_resource = boto3.resource("dynamodb")
table = dynamodb_resource.Table("users_db") # change name 

def handler(event, context):
    data = json.loads(event["body"])
    try:
        item={
            "id": str(uuid.uuid4()),
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




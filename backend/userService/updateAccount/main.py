import json
import boto3

def handler(event, context):
  try:
    # setup connection to dynamodb table
    # TODO: remember to switch the name of table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('name of table here!!!')
    
    # Read json and find userID
    user_data = json.loads(event['body'])
    userID = user_data['userID']

    response = table.update_item(
      Key = {
        'userID': userID
      },
      UpdateExpression="set name = :S",
      ExpressionAttributeValues={
        ':S':  user_data['name']
      },
      UpdateExpression="set rating = :N",
      ExpressionAttributeValues={
        ':N':  user_data['rating']
      },
      UpdateExpression="set profilePicture = :S",
      ExpressionAttributeValues={
        ':S':  user_data['profilePicture']
      },
      UpdateExpression="set bio = :S",
      ExpressionAttributeValues={
        ':S':  user_data['bio']
      },
      UpdateExpression="set location = :S",
      ExpressionAttributeValues={
        ':S':  user_data['location']
      }
    )

    return {
      'statuscode': 200,
      'body': json.dumps(response)
    }
  
  # Something went wrong with the delete  
  except Exception as e:
    print(f"exception: {e}")
    return {
      'statusCode': 500,
      'body': json.dumps(f'Error updating account: {str(e)}')
    }
  

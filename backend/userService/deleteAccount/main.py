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
    
    # Find the account entry on table and delete it
    # Return the account entry afterwards
    response = table.delete_item(Key={'userID': userID})
    return {
      'statuscode': 200,
      'body': json.dumps(response['Attributes'])
    }
    
  # Something went wrong with the delete  
  except Exception as e:
    print(f"exception: {e}")
    return {
      'statusCode': 500,
      'body': json.dumps(f'Error deleting account: {str(e)}')
    }

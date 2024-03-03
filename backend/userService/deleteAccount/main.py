import json
import boto3

# Initialize a DynamoDB resource and get the table.
def get_dynamodb_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return table

# Remove an item from the DynamoDB table.
def delete_account(table, userID):
    response = table.delete_item(
        Key={
            'userID': userID
        }
    )
    return response
  

def handler(event, context):
  try:
      # Retrieve table
      table_name = 'users-30144999'
      table = get_dynamodb_table(table_name)
      
      # Retrieve userID and attempt to delete account
      userID = event['header']['userID']
      response = delete_account(table, userID)
      
      return {
          'statusCode': 200,
          'body': json.dumps(response)
      }
      
  # Something went wrong with the delete  
  except Exception as e:
    print(f"exception: {e}")
    return {
      'statusCode': 500,
      'body': json.dumps(f'Error deleting account: {str(e)}')
    }

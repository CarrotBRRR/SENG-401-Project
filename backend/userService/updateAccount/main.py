import json
import boto3
import hashlib
import base64
import requests

# Initialize DynamoDB resource and get table
def get_dynamodb_table(table_name):
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table(table_name)
  return table

#  Parse the event body, convert to dictionary if needed
def parse_event_body(event_body):
  if isinstance(event_body, str):
    return json.loads(event_body)
  else:
    return event_body

# ----------------------------------------------------------------------------------------------------------------- #

# Cloudinary stuff
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

def create_query_string(dict):
    query_string = ""
    for ind, (key, value) in enumerate(dict.items()):
        query_string = f"{key}={value}" if ind == 0 else f"{query_string}&{key}={value}"
    return query_string

def sort_dict(dict, exclude):
    myKeys = list(dict.keys())
    myKeys.sort()
    for i in range(len(exclude)):
        if exclude[i] in myKeys:
            myKeys.remove(exclude[i])
    return {i: dict[i] for i in myKeys}

# ----------------------------------------------------------------------------------------------------------------- #

# Create the update expression string as well as the expression attribute values for values that changed
def create_table_query(old_entry, new_values):
  update_expression = "SET "
  expression_attribute_values = {}
  expression_attribute_names = {}

  # Create update expression and expression attribute values
  for feature, value in new_values.items():
    if value != old_entry[feature]:
      update_expression += f'#{feature} = :{feature}, '
      expression_attribute_values[f':{feature}'] = value
      expression_attribute_names[f'#{feature}'] = feature
      
    
  # Clean up update expression string
  update_expression = update_expression.rstrip(", ")
  return update_expression, expression_attribute_values, expression_attribute_names

# Update Account
def update_account(table, userID, old_entry, new_info):
    # Get update expression and expression attribute values
    update_expression, expression_attribute_values, expression_attribute_names = create_table_query(old_entry, new_info)

    # Update the account entry in DynamoDB
    response = table.update_item(
      Key = {
        'userID': userID
      },
      UpdateExpression=update_expression,
      ExpressionAttributeValues=expression_attribute_values,
      ExpressionAttributeNames=expression_attribute_names,
      ReturnValues="UPDATED_NEW"
    )
    
    return response

# ----------------------------------------------------------------------------------------------------------------- #
def handler(event, context):
  try:
    # setup connection to dynamodb table
    # and parse event body
    table = get_dynamodb_table(table_name="users-30144999")
    body = parse_event_body(event_body=event['body'])

    # Retrieve userID
    userID = body['userID'] 
    
    # Get old entry if it exists otherwise return 404
    response = table.get_item(Key={'userID': userID})
    if 'Item' not in response:
      # User not found
      return {
          'statusCode': 404,
          'body': 'User not found'
      }
    old_entry = response['Item']
    
    # Retrieve new table entry info turn it to a dictionary
    new_info = {
      'userID': userID,
      'name': body['name'],
      'email': body['email'],
      'rating': body['rating'],
      'bio': body['bio'],
      'location': body['location']
    }
    
    # Get old entry
    old_entry = dict(table.get_item(Key={'userID': userID}))

    # Check if image is different from old one
    raw_image = body['image']
    image_bytes = base64.b64decode(raw_image)
    new_image_hash = hashlib.sha256(image_bytes).hexdigest()
    
    # Add image hash to new info if its different
    (new_image_hash != old_entry['imageHash'])
    
    if ("imageHash" not in old_entry) or (new_image_hash != old_entry['imageHash']):
      response = post_image(image_bytes)
      new_info['profilePicture'] = response["secure_url"]
      new_info['imageHash'] = new_image_hash

    # Update the account
    response = update_account(table, userID, old_entry, new_info)

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
  

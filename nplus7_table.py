import boto3
import os
import json

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "./.aws/credentials"

# Get the service resource.
dynamodb = boto3.resource('dynamodb',region_name='us-west-1')

#DELETES PREVIOUS TABLE
table = dynamodb.Table('table name here')
try:
	table.delete()
	table.meta.client.get_waiter('table_not_exists').wait(TableName='table name here')
except:
	pass
# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='table name here',
    KeySchema=[
		{
			'AttributeName': 'word',
			'KeyType': 'HASH'
		}
    ],
	 AttributeDefinitions=[
	{
        'AttributeName': 'word',
        'AttributeType': 'S'
    }

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 25
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='table name here')

# Print out some data about the table.
print(table.item_count)
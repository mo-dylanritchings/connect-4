import json
import os
import boto3
from boto3.dynamodb.conditions import Key

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['WIN_TABLE_NAME'])

def getter(event, context):
    response = table.scan()
    items = response["Items"]

    print('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': {
            "items": items
        }
    }

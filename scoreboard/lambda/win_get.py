import json
import os

import boto3

ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['WIN_TABLE_NAME'])
_lambda = boto3.client('lambda')


def getter(event, context):
    print('request: {}'.format(json.dumps(event)))

    table.scan()

    resp = _lambda.invoke(
        FunctionName=os.environ['DOWNSTREAM_FUNCTION_NAME'],
        Payload=json.dumps(event),
    )

    body = resp['Payload'].read()

    print('downstream response: {}'.format(body))
    return json.loads(body)

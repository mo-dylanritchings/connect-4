import json
import boto3
import os

dynamo = boto3.client('dynamodb', region_name='eu-west-2')
table_name= os.environ["TABLE_NAME"]

def respond(err, response=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(response),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    operation = event['httpMethod']

    if operation == 'POST':
        json_body = event['body']
        body = json.loads(json_body)
        player  = body.get("player")

        output= update_scoreboard(player)

    elif operation == 'GET':
        output=get_scoreboard()

    else:
        return 'Error: ' + operation

    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }

def update_scoreboard(player):
    ddb_response =  dynamo.get_item(TableName=table_name, Key={'player': {'S': player}})#, ProjectionExpression='Score')

    try:
        score = ddb_response.get('Item').get('Score').get("N")
    except:
        score = 0

    score_int = int(score) + 1

    update_table = dynamo.update_item(TableName=table_name, Key={'player': {'S': player}},
                                      ExpressionAttributeNames={'#s': 'Score'},
                                      ExpressionAttributeValues={':s': {'N': str(score_int)}},
                                      UpdateExpression='SET #s = :s')
    return(update_table)

def get_scoreboard():

    score_results = dynamo.scan(TableName=table_name)
    score_items = score_results['Items']
    score_dict = {}
    for n in score_items:

        player=n.get("player").get("S")
        score=n.get("Score").get("N")
        score_dict[player] = score

    return score_dict


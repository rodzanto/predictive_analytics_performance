import json
import boto3
import time
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('leaderboard')

def lambda_handler(event, context):
    
    body = json.loads(event['body'])
    if not 'name' in body or not 'score' in body:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Missing score data in " + str(event))
        }

    try:
        table.put_item(
            Item = {
                'name': body['name'],
                'score': Decimal(str(body['score'])),
                'order': 'ORDERED',
                'timestamp': int(time.time())
            }
        )
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({})
        }
    except Exception as ex:
        print("a")
        print(ex)
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps("Server error while updating leaderboard: " + str(ex))
        }

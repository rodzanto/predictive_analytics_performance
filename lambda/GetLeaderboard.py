from decimal import Decimal
import json
import boto3
import operator
from boto3.dynamodb.conditions import Key, Attr
from operator import itemgetter, attrgetter

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('leaderboard')

def lambda_handler(event, context):
    
    response = table.query(
        KeyConditionExpression=Key('order').eq('ORDERED'),
        IndexName='order-score-index',
        ScanIndexForward=True
    )
    
    items = response['Items']
    for element in items: 
        del element['order']

    items=sorted(items, key = lambda i: (i['score'], i['timestamp']), reverse=False) 

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(items, cls=DecimalEncoder)
    }

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

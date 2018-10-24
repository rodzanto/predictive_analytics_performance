from decimal import Decimal
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AR_r_bring_your_own')

def lambda_handler(event, context):
    
    if not 'pathParameters' in event or not 'key' in event['pathParameters']:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing model key in " + str(event))
        }
    
    response = table.get_item(
        Key={
            'parameters': event['pathParameters']['key']
        }
    )
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response['Item'], cls=DecimalEncoder)
    }

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

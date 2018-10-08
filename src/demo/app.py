import json
import os

def lambda_handler(event,context):

    body={
        'environment': os.environ['Environment'],
        'status':'success!!'
    }

    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }

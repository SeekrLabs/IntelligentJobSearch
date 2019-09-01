import json
import boto3
import botocore.vendored.requests as requests
import os
from .elasticsearch import ESQuery
from .messenger import MessengerGalleryResponse

region = os.environ['AWS_REGION']
service = 'es'
credentials = boto3.Session().get_credentials()

host = os.environ['DOMAIN_ENDPOINT']
index = os.environ['DOMAIN_INDEX']

url = host + '/' + index + '/' + '_search'

def search(event, context):
    q = ESQuery(event, url)
    q.build_query()
    resp = q.send_to_es()
    print(json.loads(resp))

    out = MessengerGalleryResponse(resp).process()
    print(out)
    return {
        'statusCode': 200,
        'body': json.dumps(out)
    }
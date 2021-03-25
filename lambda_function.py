import boto3
import webcrawler,webcrawler3, webcrawler4
import requests
import datetime
import sys

def lambda_handler(event, context):
    
    sys.setrecursionlimit(9000000)
    # res = put_movie(webcrawler.excute_webcrawler())
    # res3 = put_movie(webcrawler3.excute_webcrawler3())
    res4 = put_movie(webcrawler4.excute_webcrawler4())
    print(res4)
    return ("sucess")
    
def put_movie(webresult, dynamodb=None):
    dynamodb = boto3.resource('dynamodb')
    print("1")
    table = dynamodb.Table('Allenlee_webcrawler')
    print("2")
    for i in webresult:
        print("3")
        response = table.put_item(
           Item=i
        )
        print("4")
    print("sucess!")

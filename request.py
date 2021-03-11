from bs4 import BeautifulSoup
import requests
import re
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def lambda_handler(event, context):

    try:
        for record in event['Records']:

            if record['eventName'] == 'INSERT':
                handle_insert(record)
            elif record['eventName'] == 'MODIFY':
                handle_modify(record)
            elif record['eventName'] == 'REMOVE':
                handle_remove(record)


    except Exception as e:
        print(e)
        return "Something Wrong"

def handle_insert(record):
    print('Handing INSERT event')

    newImage = record['dynamodb']['NewImage']

    newName = newImage['Name']['S']

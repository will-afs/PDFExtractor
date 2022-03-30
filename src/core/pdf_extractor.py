from src.core.pdf_extractor_utils import extract_pdf

import json
import toml
import validators

config = toml.load('settings/config.toml')
cooldown_manager_uri = config['Cooldown Manager']['cooldown_manager_uri']

def lambda_handler(event, context):
    # 1 - parse query parameters
    if not validators.url(event['uri']):
        status = 400
        message = "Incorrect format for \'uri\' argument. Expected an url-like string"
        body = {}
    elif type(event['title'])!=str:
        status = 400
        message = "Incorrect format for \'title\' argument. Expected a string"
        body = {}
    elif type(event['authors'])!=list:
        status = 400
        message = "Incorrect format for \'authors\' argument. Expected a list of strings"
        body = {}
    else:  
        pdf_metadata = {
                    'uri':event['uri'],
                    'title':event['title'],
                    'authors':event['authors'],
                }
        # 2 - construct the body of the response object
        pdf_dict = extract_pdf(pdf_metadata, cooldown_manager_uri)
        status = 200
        message = 'Success'
        body = pdf_dict
    # 3 - construct the http response
    http_response = {
        'status':status,
        'headers':{
            'Content-Type':'application/json'
        },
        'message':message,
        'body': body

    }
    # 4 - return the http response
    return http_response
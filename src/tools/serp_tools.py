import os
import json
import requests

def search_internet(query):
    """Useful to search the internet
    about a given topic and return relevant results"""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['organic']

    return results

def get_knowledge_graph(query):
    """Useful to search the internet
    about a given topic and return relevant results"""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code != 200:
        return {
            "status": "failed"
        }

    if 'knowledgeGraph' in response.json().keys():
        return {
            "status": "success",
            "kg": response.json()['knowledgeGraph']
        }
    else:
        return {
            "status": "failed"
        }


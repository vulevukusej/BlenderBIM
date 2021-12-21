import requests
import json

def get_blender_content():
    #Sign in to Azure
    url = ""

    payload=''
    headers = {    }

    response = requests.request("POST", url, headers=headers, data=payload)

    jsonData = json.loads(response.text)
    token = jsonData["access_token"]

    #Get Blender Content
    url = "0"

    payload={}
    headers = {
    'Authorization': f'Bearer {token}',
    'Cookie': '; ARRAffinitySameSite='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    return response.text


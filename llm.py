"""
Utility functions to call the OpenAI API
"""
from gc import collect
from secrets import OPENAI_API_KEY

from ujson import loads
from urequests import post

# Variables to call the API
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + OPENAI_API_KEY
}

API_URL = "https://api.openai.com/v1/chat/completions"

def call_openai(prompt):
    data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        
    collect()

    response = None
    try:
        response = post(API_URL, headers=HEADERS, json=data)
        print("Response: {}".format(response))
    except OSError as e:
        print("No Response Error: {}".format(e))
        pass
    
    collect()
    content = ''
    if response:
        if response.status_code == 200:
            response_data = loads(response.text)
            content = response_data["choices"][0]["message"]["content"].strip()
        else:
            print('Error:', response.status_code, response.text)
            # content = "I'm sorry I couldn't call the API. You might want to check your wifi. ({})".format(response.status_code)
            content += '*'
    else:
        # content = "I'm sorry something went wrong. There's no response so have a croissant."
        content += '*'
    
    collect()
    return content

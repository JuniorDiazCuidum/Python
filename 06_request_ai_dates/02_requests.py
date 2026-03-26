

import urllib.request
import json

api_post = "https://jsonplaceholder.typicode.com/posts"

try: 
    response = urllib.request.urlopen(api_post)
    data = response.read()
    json_data = json.loads(data.decode("utf-8"))
    print(json_data)
    response.close()
    
except urllib.error.URLError as e:
    print(f"Error: {e}")

import requests

print("\nGET:")
api_posts = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(api_posts)
json = response.json()
print(json[0])

print("\nPOST:")
try:
    api_posts = "https://jsonplaceholder.typicode.com/posts"
    input={
        "title": "foo",
        "body": "bar",
        "userId": 5
    }
    response = requests.post(api_posts, json=input)
    json = response.json()
    print(json)
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

OPENAIKEY = "sk-XXXXXXX"

import json

def call_openai_gpt(api_key, prompt):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4o-mini",
        "prompt": prompt,
        "max_tokens": 50
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()
api_response = call_openai_gpt(OPENAIKEY, "Cual es la capital de Francia?")


# print(json.dumps(api_response, indent=2))
print(api_response['choices'][0]['message']['content'])



import os
import requests

API_KEY = os.getenv("BUFFER_API_KEY")

url = "https://api.bufferapp.com/1/profiles.json"

params = {
    "access_token": API_KEY
}

response = requests.get(url, params=params)

print("STATUS:", response.status_code)
print(response.text)

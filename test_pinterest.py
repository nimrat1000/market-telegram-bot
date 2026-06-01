import os
import requests

TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")

url = "https://api.pinterest.com/v5/user_account"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)
print(response.text)

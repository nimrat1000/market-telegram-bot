import os
import requests

API_KEY = os.getenv("BUFFER_API_KEY")

url = "https://api.buffer.com/graphql"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

query = {
    "query": """
    query {
      me {
        id
      }
    }
    """
}

response = requests.post(url, headers=headers, json=query)

print("STATUS:", response.status_code)
print(response.text)

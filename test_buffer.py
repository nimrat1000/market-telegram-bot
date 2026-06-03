import os
import requests

API_KEY = os.getenv("BUFFER_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(
    "https://api.buffer.com/graphql",
    headers=headers
)

print("STATUS:", response.status_code)
print(response.text[:500])

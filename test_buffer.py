import os
import requests

API_KEY = os.getenv("BUFFER_API_KEY")

url = "https://api.buffer.com/graphql"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

mutation = {
    "query": """
    mutation {
      createIdea(input: {
        content: {
          title: "Test Market Report Idea"
          text: "This is a test idea created from GitHub Actions."
        }
      }) {
        ... on Idea {
          id
          content {
            title
            text
          }
        }
      }
    }
    """
}

response = requests.post(url, headers=headers, json=mutation)

print("STATUS:", response.status_code)
print(response.text)

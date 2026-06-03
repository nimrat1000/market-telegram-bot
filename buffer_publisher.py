import os
import requests

BUFFER_API_KEY = os.getenv("BUFFER_API_KEY")
BUFFER_CHANNEL_ID = os.getenv("BUFFER_CHANNEL_ID")

BUFFER_GRAPHQL_URL = "https://api.buffer.com/graphql"


def publish_to_buffer(title, blog_url, image_url):
    caption = f"""
📊 {title}

Daily US & Canada Market Report.

Read the full report:
{blog_url}

Market image:
{image_url}

#StockMarket #Investing #DividendInvesting #CanadaInvesting #MarketReport
"""

    headers = {
        "Authorization": f"Bearer {BUFFER_API_KEY}",
        "Content-Type": "application/json"
    }

    mutation = {
        "query": """
        mutation CreatePost($input: CreatePostInput!) {
          createPost(input: $input) {
            ... on PostActionSuccess {
              post {
                id
              }
            }
            ... on MutationError {
              message
            }
          }
        }
        """,
       "variables": {
            "input": {
                "text": caption,
                "channelId": BUFFER_CHANNEL_ID,
                "schedulingType": "automatic",
                "mode": "addToQueue",
                "assets": [
                    {
                        "image": {
                            "url": image_url
                }
            }
        ]
    }
}

    response = requests.post(BUFFER_GRAPHQL_URL, headers=headers, json=mutation)

    print("BUFFER STATUS:", response.status_code)
    print("BUFFER RESPONSE:", response.text)

    response.raise_for_status()
    return response.json()

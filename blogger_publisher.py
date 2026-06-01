import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


BLOG_ID = os.getenv("BLOG_ID")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")


def get_blogger_service():
    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/blogger"]
    )

    return build("blogger", "v3", credentials=creds)


def publish_market_post(title, report_text, image_url):
    service = get_blogger_service()

    content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>{title}</h2>

        <p><strong>Automated US & Canada Market Report</strong></p>

        <img src="{image_url}" alt="Daily Market Brief" style="max-width:100%; height:auto;" />

        <h3>Market Report</h3>
        <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">{report_text}</pre>

        <hr />

        <h3>Disclaimer</h3>
        <p>
        This article is generated automatically using publicly available market data and automation tools.
        The information provided is for educational and informational purposes only and should not be considered
        financial, investment, legal, tax, or professional advice.
        </p>

        <p>
        Investing involves risk, including possible loss of principal. Past performance does not guarantee future results.
        Always conduct your own research and consult a qualified professional before making financial decisions.
        </p>
    </div>
    """

    post_body = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }

    post = service.posts().insert(
        blogId=BLOG_ID,
        body=post_body,
        isDraft=False
    ).execute()

    return post.get("url")

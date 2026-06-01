import os
import requests
from datetime import datetime
import yfinance as yf
import cloudinary
import cloudinary.uploader
from PIL import Image, ImageDraw, ImageFont
from blogger_publisher import publish_market_post

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

WATCHLIST = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI",
    "VIX": "^VIX",
    "TSX Canada": "^GSPTSE",
    "USD/CAD": "CAD=X",
    "Gold": "GC=F",
    "Oil": "CL=F",
    "Bitcoin": "BTC-USD",
    "HDIF": "HDIF.TO",
    "HHIC": "HHIC.TO",
    "CDAY": "CDAY.TO",
    "SDAY": "SDAY.TO",
    "RIDH": "RIDH.TO",
    "FCGI": "FCGI.TO",
}

import cloudinary
import cloudinary.uploader
def generate_market_commentary(results):
    spx = results.get("S&P 500", (0, 0))[1]
    vix = results.get("VIX", (0, 0))[1]
    oil = results.get("Oil", (0, 0))[1]
    gold = results.get("Gold", (0, 0))[1]
    btc = results.get("Bitcoin", (0, 0))[1]
    tsx = results.get("TSX Canada", (0, 0))[1]

    # Market Mood
    if spx > 0 and vix < 0:
        mood = "Bullish"
        risk_score = 3
    elif spx < 0 and vix > 0:
        mood = "Bearish"
        risk_score = 8
    else:
        mood = "Neutral"
        risk_score = 5

    summary = f"""
📊 Market Summary

North American markets showed {'broad strength' if spx > 0 else 'mixed performance'} today.
The S&P 500 moved {spx:+.2f}% while the TSX gained {tsx:+.2f}%.
Volatility {'declined' if vix < 0 else 'increased'}, indicating {'improving investor confidence' if vix < 0 else 'rising market caution'}.

🤖 AI Outlook

Current market conditions remain {mood.lower()}.
{'Falling volatility combined with rising equity prices suggests a favorable environment for risk assets.' if mood == 'Bullish' else ''}
{'Rising volatility and falling equity prices suggest investors should remain defensive.' if mood == 'Bearish' else ''}
{'Markets remain balanced with no major risk signals currently dominating sentiment.' if mood == 'Neutral' else ''}

⚠️ Risks To Watch

• VIX: {vix:+.2f}%
• Oil: {oil:+.2f}%
• Gold: {gold:+.2f}%
• Bitcoin: {btc:+.2f}%

Watch for sudden changes in volatility, energy prices, and macroeconomic data releases.

💡 Income Investor View

Income-oriented ETFs remain attractive in stable market conditions.
Dividend-focused investors should continue monitoring interest rate expectations, market volatility, and sector concentration risks.

📅 Tomorrow's Focus

• US economic releases
• Bank of Canada developments
• Oil price trend
• USD/CAD movement
• Bitcoin momentum

🧠 Risk Score: {risk_score}/10
📍 Market Mood: {mood}
"""
    return summary
    
def upload_image_to_cloudinary(image_path):
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

    upload_result = cloudinary.uploader.upload(image_path)
    return upload_result["secure_url"]
def get_font(size, bold=False):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(font_path, size)


def get_price_change(ticker):
    data = yf.download(
        ticker,
        period="5d",
        interval="1d",
        progress=False,
        auto_adjust=True
    )

    if data.empty or len(data) < 2:
        return None

    close_data = data["Close"]

    if hasattr(close_data, "columns"):
        close_data = close_data.iloc[:, 0]

    latest = float(close_data.iloc[-1])
    previous = float(close_data.iloc[-2])

    change = ((latest - previous) / previous) * 100
    return latest, change


def collect_results():
    results = {}

    for name, ticker in WATCHLIST.items():
        result = get_price_change(ticker)
        if result:
            results[name] = result

    return results


def create_market_image(results, filename="market_report.png"):
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), (8, 18, 38))
    draw = ImageDraw.Draw(img)

    title_font = get_font(64, True)
    subtitle_font = get_font(34)
    card_font = get_font(38, True)
    small_font = get_font(28)
    footer_font = get_font(24)

    # Background gradient
    for y in range(height):
        r = int(8 + (y / height) * 14)
        g = int(18 + (y / height) * 24)
        b = int(38 + (y / height) * 48)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    today = datetime.now().strftime("%B %d, %Y")

    draw.text((70, 70), "DAILY MARKET BRIEF", font=title_font, fill="white")
    draw.text((70, 150), "US + Canada Stock Market Snapshot", font=subtitle_font, fill=(190, 210, 240))
    draw.text((70, 205), today, font=small_font, fill=(160, 180, 215))

    draw.rounded_rectangle(
        [55, 290, 1025, 1500],
        radius=35,
        fill=(15, 31, 64),
        outline=(65, 100, 160),
        width=3
    )

    image_items = [
        "S&P 500",
        "Nasdaq",
        "TSX Canada",
        "Bitcoin",
        "USD/CAD",
        "VIX"
    ]

    y = 345

    for name in image_items:
        if name not in results:
            continue

        price, change = results[name]
        change_color = (65, 210, 125) if change >= 0 else (235, 90, 90)

        draw.rounded_rectangle(
            [90, y, 990, y + 145],
            radius=24,
            fill=(22, 43, 86)
        )

        display_name = "TSX" if name == "TSX Canada" else name

        if name == "Bitcoin":
            price_text = f"${price:,.0f}"
        elif name == "USD/CAD":
            price_text = f"{price:.4f}"
        else:
            price_text = f"{price:,.2f}"

        draw.text((125, y + 28), display_name, font=card_font, fill="white")
        draw.text((125, y + 86), price_text, font=small_font, fill=(185, 205, 235))
        draw.text((760, y + 50), f"{change:+.2f}%", font=card_font, fill=change_color)

        y += 175

    risk_score = calculate_risk_score(results)
    mood = get_market_mood(risk_score)

    draw.rounded_rectangle(
        [90, 1385, 990, 1475],
        radius=24,
        fill=(25, 55, 100)
    )

    draw.text(
        (125, 1410),
        f"Risk Score: {risk_score}/10   Mood: {mood}",
        font=small_font,
        fill="white"
    )

    draw.rounded_rectangle(
        [55, 1560, 1025, 1770],
        radius=35,
        fill=(245, 248, 255)
    )

    draw.text((85, 1598), "Read the full AI market report", font=card_font, fill=(10, 25, 50))
    draw.text((85, 1660), "US markets • TSX • USD/CAD • Bitcoin • ETFs", font=small_font, fill=(40, 70, 110))
    draw.text((85, 1720), "New update every weekday morning", font=small_font, fill=(40, 70, 110))

    draw.text(
        (70, 1840),
        "Educational content only • Not financial advice",
        font=footer_font,
        fill=(180, 195, 220)
    )

    img.save(filename)
    return filename


def calculate_risk_score(results):
    score = 5

    vix = results.get("VIX")
    sp500 = results.get("S&P 500")
    nasdaq = results.get("Nasdaq")
    bitcoin = results.get("Bitcoin")

    if vix:
        vix_price, vix_change = vix
        if vix_price > 25:
            score += 2
        elif vix_price < 18:
            score -= 1

    if sp500 and sp500[1] < -1:
        score += 1
    elif sp500 and sp500[1] > 1:
        score -= 1

    if nasdaq and nasdaq[1] < -1:
        score += 1

    if bitcoin and bitcoin[1] < -2:
        score += 1

    return max(1, min(10, score))


def get_market_mood(risk_score):
    if risk_score <= 3:
        return "Constructive"
    elif risk_score <= 6:
        return "Neutral"
    return "Risk-Off"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    response.raise_for_status()


def send_telegram_photo(image_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(image_path, "rb") as image:
        files = {"photo": image}
        data = {
            "chat_id": CHAT_ID,
            "caption": caption
        }

        response = requests.post(url, data=data, files=files)
        response.raise_for_status()


def build_report(results):
    today = datetime.now().strftime("%B %d, %Y")
    message = f"📊 Daily US & Canada Market Report\n{today}\n\n"

    message += "🇺🇸 US Market\n"
    for name in ["S&P 500", "Nasdaq", "Dow Jones", "VIX"]:
        if name in results:
            price, change = results[name]
            message += f"- {name}: {price:.2f} ({change:+.2f}%)\n"

    message += "\n🇨🇦 Canada / Macro\n"
    for name in ["TSX Canada", "USD/CAD", "Gold", "Oil", "Bitcoin"]:
        if name in results:
            price, change = results[name]
            message += f"- {name}: {price:.2f} ({change:+.2f}%)\n"

    message += "\n📌 My ETF Watchlist\n"
    for name in ["HDIF", "HHIC", "CDAY", "SDAY", "RIDH", "FCGI"]:
        if name in results:
            price, change = results[name]
            message += f"- {name}: ${price:.2f} ({change:+.2f}%)\n"

    risk_score = calculate_risk_score(results)
    mood = get_market_mood(risk_score)

    message += f"\n🧠 Risk Score: {risk_score}/10"
    message += f"\n📍 Market Mood: {mood}"
    message += "\n\n⚠️ Not financial advice. For tracking only."
    message += generate_market_commentary(results)
    
    return message


if __name__ == "__main__":
    results = collect_results()

    report = build_report(results)
    print(report)

    image_path = create_market_image(results)

    image_url = upload_image_to_cloudinary(image_path)
    blog_title = f"Daily US & Canada Market Report - {datetime.now().strftime('%B %d, %Y')}"
    blog_url = publish_market_post(blog_title, report, image_url)

    send_telegram_photo(
        image_path,
        "📊 Daily Market Brief\nUS + Canada market snapshot\n\nNot financial advice."
    )

    send_telegram(f"✅ Image uploaded successfully:\n{image_url}")
    send_telegram(f"✅ Blogger post published:\n{blog_url}")

    send_telegram(report)

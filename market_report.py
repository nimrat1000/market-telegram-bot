
import os
import requests
from datetime import datetime
import yfinance as yf

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

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    response.raise_for_status()

def build_report():
    today = datetime.now().strftime("%B %d, %Y")
    message = f"📊 Daily US & Canada Market Report\n{today}\n\n"

    results = {}
    for name, ticker in WATCHLIST.items():
        result = get_price_change(ticker)
        if result:
            results[name] = result

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
            message += f"- {name}: {price:.2f} ({change:+.2f}%)\n"

    message += "\n⚠️ Not financial advice. For tracking only."
    return message

if __name__ == "__main__":
    report = build_report()
    print(report)
    send_telegram(report)

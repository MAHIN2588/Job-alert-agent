import os
import requests

def send_telegram(message):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": message
    })

def main():
    print("✅ Agent running...")
    send_telegram("✅ Job Alert Agent কাজ করছে!")
    print("✅ Telegram message sent!")

if __name__ == "__main__":
    main()
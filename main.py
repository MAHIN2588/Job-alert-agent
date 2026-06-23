import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def get_jobs():
    """Scrape remote Python jobs from RemoteOK"""
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://remoteok.com/remote-python-jobs"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
    except requests.RequestException as exc:
        print(f"❌ Failed to fetch jobs: {exc}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []
    for row in soup.find_all("tr", class_="job")[:5]:
        title_tag = row.find("h2", itemprop="title")
        company_tag = row.find("h3", itemprop="name")
        link_tag = row.get("data-url")

        if title_tag and company_tag:
            jobs.append({
                "title": title_tag.text.strip(),
                "company": company_tag.text.strip(),
                "link": f"https://remoteok.com{link_tag}" if link_tag else "N/A"
            })
    return jobs

def send_telegram(token, chat_id, message):
    """Send a message via Telegram bot"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        res = requests.post(url, json={
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=15)
        res.raise_for_status()
    except requests.RequestException as exc:
        print(f"❌ Telegram API error: {exc}")
        if hasattr(exc, "response") and exc.response is not None:
            print(f"Telegram response: {exc.response.text}")
        return False

    try:
        data = res.json()
    except ValueError:
        print(f"❌ Telegram response was not valid JSON: {res.text}")
        return False

    if not data.get("ok"):
        print(f"❌ Telegram API returned an error: {data}")
        return False

    return True

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or os.environ.get("CHAT_ID")

    if not token or not chat_id:
        print("❌ Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID/CHAT_ID")
        return

    print("🔍 Fetching jobs...")
    jobs = get_jobs()

    if not jobs:
        send_telegram(token, chat_id, "⚠️ No jobs found today.")
        print("⚠️ No jobs found.")
        return

    message = "🚀 *Latest Remote Python Jobs*\n\n"
    for i, job in enumerate(jobs, 1):
        message += f"{i}\\. *{job['title']}* at {job['company']}\n🔗 {job['link']}\n\n"

    if send_telegram(token, chat_id, message):
        print("✅ Alert sent!")
    else:
        print("❌ Failed to send Telegram notification.")

if __name__ == "__main__":
    main()
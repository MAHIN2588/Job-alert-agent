import os
import requests
from bs4 import BeautifulSoup

def scrape_bdjobs():
    url = "https://jobs.bdjobs.com/jobsearch.asp?txtsearch=&fcat=0&fcattype=0&fAreaId=6"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')

        jobs = []
        job_items = soup.find_all('div', class_='job-title-box')

        for item in job_items[:10]:
            try:
                title_el = item.find('a')
                title = title_el.text.strip() if title_el else "N/A"

                company_el = item.find('span', class_='comp-name-mbl')
                company = company_el.text.strip() if company_el else "N/A"

                jobs.append(f"📌 {title}\n🏢 {company}")
            except:
                continue

        return jobs

    except Exception as e:
        return [f"Error: {e}"]


def send_telegram(message):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": message})


def main():
    print("BDJobs থেকে job খুঁজছি...")
    jobs = scrape_bdjobs()

    if jobs:
        message = f"🔔 BDJobs — {len(jobs)} টা job:\n\n"
        message += "\n\n".join(jobs[:5])
        send_telegram(message)
        print(f"✅ {len(jobs)} টা job Telegram এ পাঠানো হয়েছে")
    else:
        print("❌ কোনো job পাইনি")
        send_telegram("⚠️ এবার কোনো job পাইনি")


if __name__ == "__main__":
    main()
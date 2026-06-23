import os
import requests
from bs4 import BeautifulSoup


# ===== SCRAPER 1: BDJobs =====
def scrape_bdjobs():
    url = "https://jobs.bdjobs.com/jobsearch.asp?txtsearch=&fcat=0&fcattype=0&fAreaId=6"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        jobs = []
        for item in soup.find_all('div', class_='job-title-box')[:10]:
            try:
                title = item.find('a').text.strip()
                company_el = item.find('span', class_='comp-name-mbl')
                company = company_el.text.strip() if company_el else "N/A"
                jobs.append({"title": title, "company": company, "source": "BDJobs"})
            except:
                continue
        return jobs
    except Exception as e:
        print(f"BDJobs error: {e}")
        return []


# ===== SCRAPER 2: Chakri.com =====
def scrape_chakri():
    url = "https://www.chakri.com/jobs"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        jobs = []
        for item in soup.find_all('div', class_='job-item')[:10]:
            try:
                title_el = item.find('h2') or item.find('h3') or item.find('a')
                title = title_el.text.strip() if title_el else "N/A"
                company_el = item.find('span', class_='company')
                company = company_el.text.strip() if company_el else "N/A"
                if title != "N/A":
                    jobs.append({"title": title, "company": company, "source": "Chakri"})
            except:
                continue
        return jobs
    except Exception as e:
        print(f"Chakri error: {e}")
        return []


# ===== SCRAPER 3: Prothomalo =====
def scrape_prothomalo():
    url = "https://www.prothomalo.com/chakri"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        jobs = []
        for item in soup.find_all('article')[:10]:
            try:
                title_el = item.find('h3') or item.find('h2')
                title = title_el.text.strip() if title_el else "N/A"
                if title != "N/A" and len(title) > 3:
                    jobs.append({"title": title, "company": "N/A", "source": "Prothomalo"})
            except:
                continue
        return jobs
    except Exception as e:
        print(f"Prothomalo error: {e}")
        return []


# ===== TELEGRAM =====
def send_telegram(message):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    })


# ===== MAIN =====
def main():
    all_jobs = []

    print("BDJobs scraping...")
    bdjobs = scrape_bdjobs()
    all_jobs.extend(bdjobs)
    print(f"  → {len(bdjobs)} jobs")

    print("Chakri scraping...")
    chakri = scrape_chakri()
    all_jobs.extend(chakri)
    print(f"  → {len(chakri)} jobs")

    print("Prothomalo scraping...")
    prothomalo = scrape_prothomalo()
    all_jobs.extend(prothomalo)
    print(f"  → {len(prothomalo)} jobs")

    print(f"\nTotal: {len(all_jobs)} jobs found")

    if all_jobs:
        sources = {}
        for job in all_jobs:
            src = job['source']
            if src not in sources:
                sources[src] = []
            sources[src].append(job)

        message = f"🔔 <b>Job Alert — {len(all_jobs)} টা job</b>\n\n"

        for source, jobs in sources.items():
            if jobs:
                message += f"📍 <b>{source}</b>\n"
                for job in jobs[:3]:
                    message += f"  📌 {job['title']}\n"
                    if job['company'] != "N/A":
                        message += f"  🏢 {job['company']}\n"
                message += "\n"

        send_telegram(message)
        print("✅ Telegram এ পাঠানো হয়েছে")
    else:
        print("❌ কোনো job পাইনি")
        send_telegram("⚠️ এবার কোনো job পাইনি")


if __name__ == "__main__":
    main()
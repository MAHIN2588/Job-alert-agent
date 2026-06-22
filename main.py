import os

def main():
    print("✅ Job Alert Agent running!")
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    if telegram_token:
        print("✅ Telegram token found")
    else:
        print("❌ Telegram token missing")

if __name__ == "__main__":
    main()
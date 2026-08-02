import os, json, time, sys
import requests

TOKEN = os.environ.get("BOT_TOKEN", "8591869743:AAFgSoVueO9FXIVjIPgwOnDIPOeeN_5x05s")
ADMIN_ID = os.environ.get("ADMIN_ID", "903104535")
API_URL = os.environ.get("API_URL", "https://vexiostudio.ru")

HEADERS = {
    "HR": "\U0001F465 Новая заявка — Vexio HR",
    "BRIEF": "\U0001F4CB Новая заявка — Vexio Brief",
    "SITE": "\U0001F4E6 Новая заявка — Vexio Studio"
}

def format_hr(data):
    return (
        f"\U0001F464 Имя: {data.get('name', '—')}\n"
        f"\U0001F4F1 Телефон: {data.get('phone', '—')}\n"
        f"\U0001F4AC Telegram: @{data.get('telegram', '—')}\n"
        f"\U0001F4BC Вакансия: {data.get('position', '—')}"
    )

def format_brief(data):
    return (
        f"\U0001F4E6 Формат: {data.get('format', '—')}\n"
        f"\U0001F3E2 Бизнес: {data.get('business', '—')}\n"
        f"\U0001F3AF Цель: {data.get('goal', '—')}\n"
        f"\U0001F4DE Контакт: {data.get('contact', '—')}\n"
        f"\U0001F310 Сайт: {data.get('website', '—')}"
    )

def format_site(data):
    return (
        f"\U0001F464 Имя: {data.get('name', '—')}\n"
        f"\U0001F4CB Проект: {data.get('project', '—')}\n"
        f"\U0001F4F1 Телефон: {data.get('phone', '—')}\n"
        f"\U0001F3D7 Тип: {data.get('type', '—')}\n"
        f"\U0001F4DD Описание: {data.get('description', '—')}\n"
        f"\U0001F6CD Каталог: {data.get('catalog', 'no')}\n"
        f"\u2699 Админка: {data.get('admin', 'no')}\n"
        f"\u2708 Telegram бот: {data.get('telegram', 'no')}"
    )

def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": ADMIN_ID, "text": msg, "parse_mode": "HTML"},
            timeout=5
        )
    except Exception as e:
        print(f"Send error: {e}")

def main():
    sent = set()
    while True:
        try:
            r = requests.get(f"{API_URL}/api/notifications", timeout=5)
            items = r.json()
            for item in items:
                key = item.get("time", "") + item.get("source", "")
                if key in sent:
                    continue
                source = item["source"].upper()
                header = HEADERS.get(source, f"Новая заявка — {source}")
                data = item["data"]
                if source == "HR":
                    body = format_hr(data)
                elif source == "BRIEF":
                    body = format_brief(data)
                else:
                    body = format_site(data)
                send(f"<b>{header}</b>\n\n{body}")
                sent.add(key)
            if items:
                requests.post(f"{API_URL}/api/notifications/clear", timeout=5)
                sent.clear()
        except Exception as e:
            print(f"Poll error: {e}")
        time.sleep(10)

if __name__ == "__main__":
    print("Bot started")
    main()

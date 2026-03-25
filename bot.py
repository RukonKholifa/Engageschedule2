import telebot
import schedule
import time
import requests
import threading
from flask import Flask
from datetime import datetime, timedelta
import pytz

TOKEN = '8651930798:AAH9777sWQpkj7z3dHyFpC0M6hyme7GbjPk'
GROUP_CHAT_ID = '-1003702085290'
MENTIONS = "@Rukon_kholifa @TouFiqVH @RDX_NARUTO @Didarul_Habib96 @Sure_Ahmmed"

bot = telebot.TeleBot(TOKEN)
bdt = pytz.timezone('Asia/Dhaka')

sessions = [
    {
        "gc": "Hidden Mafia",
        "link": "https://t.me/c/3521163148/83",
        "times": ["13:00", "05:00", "20:00", "01:00"]
    },
    {
        "gc": "SilentAlpha",
        "link": "https://t.me/SilentAlphaGroup",
        "times": ["11:00", "14:00", "17:00", "20:00", "23:00"]
    },
    {
        "gc": "Spherical HUB",
        "link": "https://t.me/+juerAsiSRNk4MjVk",
        "times": ["13:00", "17:00", "21:00", "01:00"]
    }
]

sent_alerts = set()

app = Flask(name)

@app.route('/')
def home():
    return "GC Alert Bot Live!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    while True:
        try:
            requests.get("https://engageschedule2-1.onrender.com", timeout=10)
        except:
            pass
        time.sleep(300)

def check_and_alert():
    global sent_alerts
    try:
        now = datetime.now(bdt)
        current_minute = now.strftime("%H:%M")
        target_time = (now + timedelta(minutes=5)).strftime("%H:%M")

        for item in sessions:
            for t in item["times"]:
                alert_id = f"{item['gc']}_{t}_{current_minute}"

                if t == target_time and alert_id not in sent_alerts:
                    msg = (
                        f"⚡️ ৫ মিনিট বাকি!\n\n"
                        f"📌 GC Name: {item['gc']}\n"
                        f"🔗 Link: {item['link']}\n\n"
                        f"{MENTIONS}"
                    )

                    bot.send_message(
                        GROUP_CHAT_ID,
                        msg,
                        disable_web_page_preview=True
                    )

                    sent_alerts.add(alert_id)
                    print(f"Sent reminder for {item['gc']} at {t}")

        if current_minute == "00:00":
            sent_alerts.clear()

    except Exception as e:
        print(f"Error: {e}")

schedule.every(30).seconds.do(check_and_alert)

if name == "main":
    threading.Thread(target=run_server).start()
    threading.Thread(target=keep_alive).start()

    while True:
        schedule.run_pending()
        time.sleep(5)

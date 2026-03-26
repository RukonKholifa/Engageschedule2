import telebot
import schedule
import time
import requests
import threading
from flask import Flask
from datetime import datetime, timedelta
import pytz

TOKEN = '8651930798:AAE28w-UGL9ONuBsS0mdgW31KKC3smfLDyw'
GROUP_CHAT_ID = '-1003702085290'

MENTIONS = (
    '<a href="tg://user?id=5542815933">Rukon</a> '
    '<a href="tg://user?id=665980342">TouFiq</a> '
    '<a href="tg://user?id=6364786244">Nabil</a> '
    '<a href="tg://user?id=6291029584">Didarul</a> '
    '<a href="tg://user?id=7510435738">Rifat</a>'
)

bot = telebot.TeleBot(TOKEN)
bdt = pytz.timezone('Asia/Dhaka')

sessions = [
    {"gc": "Hidden Mafia", "link": "https://t.me/c/3521163148/83", "times": ["13:00", "16:00", "20:00", "01:00"]},
    {"gc": "SilentAlpha", "link": "https://t.me/SilentAlphaGroup", "times": ["11:00", "14:00", "17:00", "20:00", "23:00"]},
    {"gc": "Spherical HUB", "link": "https://t.me/+juerAsiSRNk4MjVk", "times": ["13:00", "17:00", "21:00", "01:00"]}
]

sent_alerts = set()

app = Flask(__name__) # এখানে ভুল ছিল, __name__ হবে

@app.route('/')
def home():
    return "Bot Running"

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    while True:
        try:
            requests.get("https://engageschedule2-2.onrender.com", timeout=10)
        except:
            pass
        time.sleep(300)

def check_and_alert():
    global sent_alerts

    now = datetime.now(bdt)
    current_minute = now.strftime("%H:%M")
    target_time = (now + timedelta(minutes=5)).strftime("%H:%M")

    active_sessions = []

    for item in sessions:
        for t in item["times"]:
            if t == target_time:
                active_sessions.append(item)

    if active_sessions:
        alert_id = f"{target_time}_{current_minute}"

        if alert_id not in sent_alerts:
            msg = "⚡️ ৫ মিনিট বাকি!\n\n"

            for s in active_sessions:
                msg += f"📌 {s['gc']}\n🔗 {s['link']}\n\n"

            msg += MENTIONS

            bot.send_message(
                GROUP_CHAT_ID,
                msg,
                parse_mode="HTML",
                disable_web_page_preview=True
            )

            sent_alerts.add(alert_id)
            print("Combined alert sent")

    if current_minute == "00:00":
        sent_alerts.clear()

schedule.every(30).seconds.do(check_and_alert)

if __name__ == "__main__": # এখানেও ভুল ছিল, __name__ এবং "__main__" হবে
    threading.Thread(target=run_server).start()
    threading.Thread(target=keep_alive).start()

    while True:
        schedule.run_pending()
        time.sleep(5)

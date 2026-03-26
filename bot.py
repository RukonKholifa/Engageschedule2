import telebot
import schedule
import time
import requests
import threading
import os
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

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is awake and running!"

def run_server():
    # Render er standard port variable use kora safe
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    while True:
        try:
            # Nijei nijeke ping kora jate server sleep-e na jay
            requests.get("https://engageschedule2-2.onrender.com", timeout=15)
        except:
            pass
        time.sleep(180) # 3 minute por por ping

def check_and_alert():
    global sent_alerts

    # UTC theke perfect BDT timezone ensure kora
    now = datetime.now(pytz.utc).astimezone(bdt)
    current_time_str = now.strftime("%H:%M")
    
    # Target time calculate kora (5 minute porer jonno)
    target_dt = now + timedelta(minutes=5)
    target_time = target_dt.strftime("%H:%M")

    active_sessions = [s for s in sessions if target_time in s["times"]]

    if active_sessions:
        # Unique ID with Date (jate protidin eki somoy alert dite pare)
        alert_id = f"{target_time}_{now.strftime('%Y%m%d')}"

        if alert_id not in sent_alerts:
            msg = "⚡️ ৫ মিনিট বাকি!\n\n"
            for s in active_sessions:
                msg += f"📌 {s['gc']}\n🔗 {s['link']}\n\n"
            msg += MENTIONS

            try:
                bot.send_message(
                    GROUP_CHAT_ID,
                    msg,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                sent_alerts.add(alert_id)
                print(f"[{current_time_str}] Alert sent for {target_time}")
            except Exception as e:
                print(f"Error: {e}")

    # Purano alert clear kora jate memory jam na hoy
    if len(sent_alerts) > 50:
        sent_alerts.clear()

# Protir 20 second por por check kora
schedule.every(20).seconds.do(check_and_alert)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()

    print("Bot started...")
    while True:
        schedule.run_pending()
        time.sleep(1)

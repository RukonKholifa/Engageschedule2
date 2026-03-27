import telebot
import schedule
import time
import requests
import threading
import os
from flask import Flask
from datetime import datetime, timedelta
import pytz

# --- Configuration ---
TOKEN = '8651930798:AAE28w-UGL9ONuBsS0mdgW31KKC3smfLDyw'
GROUP_CHAT_ID = '-1003702085290'
# Tomar Render URL ekhane thik thakle thakuk, na thakle update koro
RENDER_URL = "https://engageschedule2-2.onrender.com" 

MENTIONS = (
    '<a href="tg://user?id=5542815933">Rukon</a> '
    '<a href="tg://user?id=665980342">TouFiq</a> '
    '<a href="tg://user?id=6364786244">Nabil</a> '
    '<a href="tg://user?id=6291029584">Didarul</a> '
    '<a href="tg://user?id=7510435738">Rifat</a>'
)

bot = telebot.TeleBot(TOKEN)
bdt = pytz.timezone('Asia/Dhaka')

# --- Sessions ---
sessions = [
    {"gc": "Hidden Mafia", "link": "https://t.me/c/3521163148/83", "times": ["13:00", "16:00", "20:00", "01:00"]},
    {"gc": "SilentAlpha", "link": "https://t.me/SilentAlphaGroup", "times": ["11:00", "14:00", "17:00", "20:00", "23:00"]},
    {"gc": "Spherical HUB", "link": "https://t.me/+juerAsiSRNk4MjVk", "times": ["13:00", "17:00", "21:00", "01:00"]}
]

sent_alerts = set()
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and watching the clock!"

def run_server():
    # Render environment variable theke port neya
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    while True:
        try:
            # Server ke awake rakhar jonno 3 minute por por ping
            requests.get(RENDER_URL, timeout=15)
            print("Pinged server to keep it awake.")
        except Exception as e:
            print(f"Keep-alive ping failed: {e}")
        time.sleep(180) 

def check_and_alert():
    global sent_alerts

    # Server-er system time ja-i houk, eta ke UTC dore BDT-te convert kora
    now_utc = datetime.now(pytz.utc)
    now_bdt = now_utc.astimezone(bdt)
    
    # Session start hobar thik 5 minute ager time check kora
    target_dt = now_bdt + timedelta(minutes=10)
    target_time = target_dt.strftime("%H:%M")

    active_sessions = [s for s in sessions if target_time in s["times"]]

    if active_sessions:
        # Unique ID with Date (Date thakle protidin ek-i time-e alert jabe)
        alert_id = f"{target_time}_{now_bdt.strftime('%Y%m%d')}"

        if alert_id not in sent_alerts:
            msg = "⚡️ <b>৫ মিনিট বাকি!</b>\n\n"
            for s in active_sessions:
                msg += f"📌 <b>{s['gc']}</b>\n🔗 {s['link']}\n\n"
            
            msg += f"👥 {MENTIONS}"

            try:
                bot.send_message(
                    GROUP_CHAT_ID,
                    msg,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                sent_alerts.add(alert_id)
                print(f"[{now_bdt.strftime('%H:%M')}] Alert sent for {target_time}")
            except Exception as e:
                print(f"Telegram error: {e}")

    # Memory clean up (50 tar beshi purano alert tracker delete kora)
    if len(sent_alerts) > 50:
        sent_alerts.clear()

# 20 second por por check kora safe
schedule.every(20).seconds.do(check_and_alert)

if __name__ == "__main__":
    # Flask and Ping logic threads-e start kora
    threading.Thread(target=run_server, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()

    print("Bot is starting and monitoring sessions...")
    while True:
        schedule.run_pending()
        time.sleep(1)

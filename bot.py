import telebot
import schedule
import time
import requests
import threading
from flask import Flask
from datetime import datetime, timedelta
import pytz

# তোমার টোকেন
TOKEN = '8651930798:AAH9777sWQpkj7z3dHyFpC0M6hyme7GbjPk'

# ইউজারদের আইডি লিস্ট
USER_IDS = [
    '5542815933', # Rukon
    '665980342',  # TouFiqVH
    '6364786244', # RDX_NARUTO
    '6291029584', # Didarul_Habib96
    '7510435738'  # Sure_Ahmmed
]

RENDER_URL = "https://engageschedule2.onrender.com"

bot = telebot.TeleBot(TOKEN)
bdt = pytz.timezone('Asia/Dhaka')

# সেশন ডেটা (৮:১৫ এর ট্রায়াল যোগ করা হয়েছে)
sessions = [
    {"gc": "Trial Session", "times": ["20:15"]}, # এই লাইনটি ট্রায়ালের জন্য
    {"gc": "Spherical HUB", "times": ["13:00", "17:00", "21:00", "01:00"]},
    {"gc": "Hidden Mafia", "times": ["13:00", "20:00", "01:00", "04:00"]},
    {"gc": "MEGA ENGAGE", "times": ["11:30", "16:30", "20:30", "00:30"]},
    {"gc": "Team Incurify", "times": ["13:00", "17:00", "22:00", "01:00"]}
]

app = Flask('')
@app.route('/')
def home():
    return "Trial Bot is Running!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    while True:
        try:
            requests.get(RENDER_URL)
        except:
            pass
        time.sleep(600)

def check_and_alert():
    try:
        now = datetime.now(bdt)
        # ৫ মিনিট পরের সময় চেক করবে
        alert_time = (now + timedelta(minutes=5)).strftime("%H:%M")
        
        for item in sessions:
            for t in item["times"]:
                if t == alert_time:
                    msg = (f"🧪 *TRIAL ALERT: {item['gc']}*\n\n"
                           f"বসেরা, এটি একটি ট্রায়াল মেসেজ।\n"
                           f"⏰ সেশন শুরুর সময়: `{t}` (BDT)")
                    
                    for user_id in USER_IDS:
                        try:
                            bot.send_message(user_id, msg, parse_mode="Markdown")
                        except:
                            pass
    except Exception as e:
        print(f"Error: {e}")

schedule.every(1).minutes.do(check_and_alert)

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    threading.Thread(target=keep_alive).start()
    
    print("--- Trial Bot is active ---")
    
    while True:
        schedule.run_pending()
        time.sleep(30)

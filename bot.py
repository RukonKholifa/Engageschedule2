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

# ইউজারদের আইডি লিস্ট (তোমার ৫টি আইডি এখানে যোগ করলাম)
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

# সেশন ডেটা
sessions = [
    {"gc": "Spherical HUB", "times": ["13:00", "17:00", "21:00", "01:00"]},
    {"gc": "Hidden Mafia", "times": ["13:00", "20:00", "01:00", "04:00"]},
    {"gc": "MEGA ENGAGE", "times": ["11:30", "16:30", "20:30", "00:30"]},
    {"gc": "Team Incurify", "times": ["13:00", "17:00", "22:00", "01:00"]}
]

# ১. ছোট একটি ওয়েব সার্ভার
app = Flask('')
@app.route('/')
def home():
    return "Multi-User Bot is Alive!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

# ২. সেলফ-পিং ফাংশন
def keep_alive():
    while True:
        try:
            requests.get(RENDER_URL)
            print("Self-ping: Awake!")
        except:
            print("Self-ping failed.")
        time.sleep(600)

# ৩. অ্যালার্ট চেক এবং সবার কাছে পাঠানো
def check_and_alert():
    try:
        now = datetime.now(bdt)
        alert_time = (now + timedelta(minutes=5)).strftime("%H:%M")
        
        for item in sessions:
            for t in item["times"]:
                if t == alert_time:
                    msg = (f"⚡ *GC ALERT: {item['gc']}*\n\n"
                           f"বসেরা রেডি হন! সেশন শুরু হতে মাত্র ৫ মিনিট বাকি।\n"
                           f"⏰ শুরুর সময়: `{t}` (BDT)")
                    
                    # লুপ চালিয়ে সবার আইডিতে মেসেজ পাঠানো
                    for user_id in USER_IDS:
                        try:
                            bot.send_message(user_id, msg, parse_mode="Markdown")
                        except Exception as send_err:
                            print(f"Could not send to {user_id}: {send_err}")
                            
    except Exception as e:
        print(f"Error: {e}")

# শিডিউল সেটআপ
schedule.every(1).minutes.do(check_and_alert)

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    threading.Thread(target=keep_alive).start()
    
    print("--- GC Multi-User Alert Bot is starting ---")
    
    # শুরুতে সবাইকে একটি অনলাইন মেসেজ দেওয়া (ইচ্ছাধীন)
    for user_id in USER_IDS:
        try:
            bot.send_message(user_id, "🚀 *GC Alert Bot* এখন আপডেট হয়েছে এবং ৫ জন ইউজারের জন্য অনলাইন আছে!", parse_mode="Markdown")
        except:
            pass

    while True:
        schedule.run_pending()
        time.sleep(30)

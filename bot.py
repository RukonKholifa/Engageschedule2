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

# Mentions thik kora hoyeche (underscore soho)
MENTIONS = "@Rukon_kholifa @TouFiqVH @RDX_NARUTO @Didarul_Habib96 @Sure_Ahmmed"

bot = telebot.TeleBot(TOKEN)
bdt = pytz.timezone('Asia/Dhaka')

sessions = [
    {"gc": "Spherical HUB", "times": ["13:00", "17:00", "21:00", "01:00"]},
    {"gc": "Hidden Mafia", "times": ["13:00", "20:00", "01:00", "04:00"]},
    {"gc": "MEGA ENGAGE", "times": ["11:30", "16:30", "20:30", "00:30"]},
    {"gc": "Team Incurify", "times": ["13:00", "17:00", "22:00", "01:00"]}
]

# Jate ek-i message bar bar na jay tar jonno tracking
sent_alerts = set()

app = Flask('')
@app.route('/')
def home(): return "GC Alert Bot - Dual Reminders Live!"

def run_server(): 
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    while True:
        try: requests.get("https://engageschedule2-1.onrender.com")
        except: pass
        time.sleep(300)

def check_and_alert():
    global sent_alerts
    try:
        now = datetime.now(bdt)
        current_minute = now.strftime("%H:%M")
        
        # Shudhu 10 ebang 5 minute agei check korbe
        t_minus_10 = (now + timedelta(minutes=10)).strftime("%H:%M")
        t_minus_5 = (now + timedelta(minutes=5)).strftime("%H:%M")

        for item in sessions:
            for t in item["times"]:
                alert_id = f"{item['gc']}_{t}_{current_minute}" # Unique ID jate repeat na hoy
                
                if alert_id not in sent_alerts:
                    reminder_text = ""
                    if t == t_minus_10:
                        reminder_text = "⚠️ **১০ মিনিট বাকি!** তৈরি হয়ে নিন।"
                    elif t == t_minus_5:
                        reminder_text = "⚡ **৫ মিনিট বাকি!** সবাই অনলাইনে আসুন।"

                    if reminder_text:
                        msg = (f"{reminder_text}\n\n"
                               f"📌 **GC: {item['gc']}**\n"
                               f"⏰ শুরুর সময়: `{t}` (BDT)\n\n"
                               f"ডাক দেওয়া হচ্ছে: {MENTIONS}")
                        bot.send_message(GROUP_CHAT_ID, msg, parse_mode="Markdown")
                        sent_alerts.add(alert_id)
                        print(f"Sent reminder for {t}")

        # Din sheshe tracker clear kora jate memory ful na hoy
        if now.strftime("%H:%M") == "00:00":
            sent_alerts.clear()
                            
    except Exception as e:
        print(f"Error: {e}")

# Check frequency komiye dewa hoyeche jate duplicate chance na thake
schedule.every(50).seconds.do(check_and_alert)

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    threading.Thread(target=keep_alive).start()
    while True:
        schedule.run_pending()
        time.sleep(10)

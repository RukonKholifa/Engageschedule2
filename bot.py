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

# যাদের মেনশন করতে চাও তাদের ইউজারনেম
MENTIONS = "@Rukon_kholifa @TouFiqVH @RDX_NARUTO @Didarul_Habib96 @Sure_Ahmmed"

bot = telebot.TeleBot(TOKEN)
bdt = pytz.timezone('Asia/Dhaka')

sessions = [
    {"gc": "Spherical HUB", "times": ["13:00", "17:00", "21:00", "01:00"]},
    {"gc": "Hidden Mafia", "times": ["13:00", "20:00", "01:00", "04:00"]},
    {"gc": "MEGA ENGAGE", "times": ["11:30", "16:30", "20:30", "00:30"]},
    {"gc": "Team Incurify", "times": ["13:00", "17:00", "22:00", "01:00"]}
]

app = Flask('')
@app.route('/')
def home(): return "GC Alert Bot is Active!"

def run_server(): 
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    while True:
        try: 
            requests.get("https://engageschedule2-1.onrender.com")
        except: 
            pass
        time.sleep(300)

def check_and_alert():
    try:
        now = datetime.now(bdt)
        
        t_minus_10 = (now + timedelta(minutes=10)).strftime("%H:%M")
        t_minus_5 = (now + timedelta(minutes=5)).strftime("%H:%M")
        t_minus_2 = (now + timedelta(minutes=2)).strftime("%H:%M")

        for item in sessions:
            for t in item["times"]:
                reminder_text = ""
                if t == t_minus_10:
                    reminder_text = "⚠️ **১০ মিনিট বাকি!** তৈরি হয়ে নিন।"
                elif t == t_minus_5:
                    reminder_text = "⚡ **৫ মিনিট বাকি!** সবাই অনলাইনে আসুন।"
                elif t == t_minus_2:
                    reminder_text = "🔥 **মাত্র ২ মিনিট!** এখনই জয়েন করার প্রস্তুতি নিন।"

                if reminder_text:
                    msg = (f"{reminder_text}\n\n"
                           f"📌 **GC: {item['gc']}**\n"
                           f"⏰ শুরুর সময়: `{t}` (BDT)\n\n"
                           f"ডাক দেওয়া হচ্ছে: {MENTIONS}")
                    bot.send_message(GROUP_CHAT_ID, msg, parse_mode="Markdown")
                    print(f"Sent reminder for {t}")
                            
    except Exception as e:
        print(f"Error: {e}")

schedule.every(30).seconds.do(check_and_alert)

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    threading.Thread(target=keep_alive).start()
    
    print("--- Multi-Reminder Bot is starting ---")
    
    while True:
        schedule.run_pending()
        time.sleep(5)

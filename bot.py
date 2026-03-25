import telebot
import schedule
import time
from datetime import datetime, timedelta
import pytz

# তোমার দেওয়া তথ্যগুলো এখানে সেট করলাম
TOKEN = '8651930798:AAH9777sWQpkj7z3dHyFpC0M6hyme7GbjPk'
CHAT_ID = '5542815933'

bot = telebot.TeleBot(TOKEN)
bdt = pytz.timezone('Asia/Dhaka')

# সেশন ডেটা (২৪ ঘণ্টার ফরম্যাটে)
sessions = [
    {"gc": "Spherical HUB", "times": ["13:00", "17:00", "21:00", "01:00"]},
    {"gc": "Hidden Mafia", "times": ["13:00", "20:00", "01:00", "04:00"]},
    {"gc": "MEGA ENGAGE", "times": ["11:30", "16:30", "20:30", "00:30"]},
    {"gc": "Team Incurify", "times": ["13:00", "17:00", "22:00", "01:00"]}
]

def check_and_alert():
    try:
        now = datetime.now(bdt)
        # ৫ মিনিট পরের সময় বের করা
        alert_time = (now + timedelta(minutes=5)).strftime("%H:%M")
        current_time_str = now.strftime("%H:%M:%S")
        
        print(f"Checking for alert at {alert_time}... (Current BDT: {current_time_str})")

        for item in sessions:
            for t in item["times"]:
                if t == alert_time:
                    msg = (f"⚡ *GC ALERT: {item['gc']}*\n\n"
                           f"বসেরা রেডি হন! সেশন শুরু হতে মাত্র ৫ মিনিট বাকি।\n"
                           f"⏰ শুরুর সময়: `{t}` (BDT)\n\n"
                           f"শুভকামনা! 🔥")
                    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                    print(f"Successfully sent alert for {item['gc']}")
    except Exception as e:
        print(f"Error: {e}")

# প্রতি ১ মিনিটে একবার করে চেক করবে
schedule.every(1).minutes.do(check_and_alert)

print("--- GC Alert Bot is starting ---")
try:
    bot.send_message(CHAT_ID, "🚀 *GC Alert Bot* এখন অনলাইন এবং আপনার পাহারায় নিয়োজিত আছে!", parse_mode="Markdown")
except Exception as e:
    print(f"Could not send welcome message: {e}")

while True:
    schedule.run_pending()
    time.sleep(30) # ৩০ সেকেন্ড পর পর লুপ চেক করবে
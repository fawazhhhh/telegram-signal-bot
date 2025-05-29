import telebot
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup

TOKEN = "8067149612:AAH8_RotPca46jwxAk9bWONzOWB6Yf56CF8"
CHAT_ID = "7890943736"

bot = telebot.TeleBot(TOKEN)

def send_signal(signal):
    bot.send_message(CHAT_ID, signal)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "✅ البوت يعمل الآن تلقائيًا، وسيتم إرسال الإشارات كل 15 ثانية.")

def analyze_market():
    try:
        url = "https://app.eobroker.com/en/trade/smart"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.text.lower()
        if "buy" in text or "شراء" in text:
            return "شراء"
        elif "sell" in text or "بيع" in text:
            return "بيع"
        else:
            return "انتظر"
    except Exception as e:
        return "انتظر"

def run():
    while True:
        signal = analyze_market()
        send_signal(signal)
        time.sleep(15)

import threading
threading.Thread(target=run).start()

bot.polling()

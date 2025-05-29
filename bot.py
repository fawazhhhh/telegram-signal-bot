import telebot
import time
import requests
from bs4 import BeautifulSoup

TOKEN = "8067149612:AAH8_RotPca46jwxAk9bWONzOWB6Yf56CF8"  # توكن البوت
CHAT_ID = "7890943736"  # معرف التليجرام

bot = telebot.TeleBot(TOKEN)

def send_signal(signal):
    bot.send_message(CHAT_ID, signal)

def analyze_market():
    try:
        url = "https://expertoption.com"  # رابط منصة EO
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.text.lower()

        if "شراء" in text or "buy" in text:
            return "شراء"
        elif "بيع" in text or "sell" in text:
            return "بيع"
        else:
            return "جاري التحليل"
    except Exception:
        return "جاري التحليل"

def run():
    while True:
        signal = analyze_market()
        send_signal(signal)
        time.sleep(60)

import threading
threading.Thread(target=run).start()

bot.polling()

import telebot
import time
import requests
from bs4 import BeautifulSoup

# بيانات البوت الحقيقية
TOKEN = "7803079502:AAE967yp04T8Gy5z66Xd8hwQsi9XfZcVcyk"
CHAT_ID = 7890943736

bot = telebot.TeleBot(TOKEN)

def send_signal(signal):
    bot.send_message(CHAT_ID, signal)

def analyze_market():
    try:
        url = "https://expertoption.com"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.text.lower()

        if "شراء" in text or "buy" in text:
            return "شراء"
        elif "بيع" in text or "sell" in text:
            return "بيع"
        else:
            return "جاري التحليل"
    except Exception:
        return "جاري التحليل"

while True:
    signal = analyze_market()
    send_signal(signal)
    time.sleep(60)

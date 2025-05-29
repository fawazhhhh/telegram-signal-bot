import telebot
from datetime import datetime

TOKEN = "8067149612:AAH8_RotPca46jwxAk9bWONzOWB6Yf56CF8"
CHAT_ID = "7890943736"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Bot is running and ready to send signals!")

def send_signal(signal):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.send_message(CHAT_ID, f"{signal} - {now}")

bot.polling()

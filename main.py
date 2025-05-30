import time
import logging
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# بيانات تليجرام
TELEGRAM_BOT_TOKEN = '7803079502:AAE967yp04T8Gy5z66Xd8hwQsi9XfZcVcyk'
CHAT_ID = '7890943736'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# إعداد المتصفح
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# إرسال إشارة لتليجرام
def send_signal_to_telegram(signal):
    try:
        bot.send_message(CHAT_ID, signal)
    except Exception as e:
        logging.error(f"فشل الإرسال: {e}")

# تحليل السوق الحقيقي
def analyze_market():
    try:
        driver = create_driver()
        driver.get("https://app.expertoption.com")
        time.sleep(15)  # انتظار تحميل الصفحة

        rsi = float(driver.find_element(By.CLASS_NAME, "rsi-indicator-value").text)
        macd_signal = driver.find_element(By.CLASS_NAME, "macd-cross-status").text.lower()
        ema_position = driver.find_element(By.CLASS_NAME, "ema-status").text.lower()
        momentum = float(driver.find_element(By.CLASS_NAME, "momentum-indicator-value").text)
        candle_pattern = driver.find_element(By.CLASS_NAME, "candle-pattern-name").text.lower()

        score = 0
        if rsi < 30:
            score += 1
        elif rsi > 70:
            score -= 1

        if "صاعد" in macd_signal:
            score += 1
        elif "نازل" in macd_signal:
            score -= 1

        if "فوق" in ema_position:
            score += 1
        elif "تحت" in ema_position:
            score -= 1

        if momentum > 0:
            score += 1
        elif momentum < 0:
            score -= 1

        if any(x in candle_pattern for x in ["hammer", "engulfing", "doji"]):
            score += 1

        if score >= 4:
            send_signal_to_telegram("شراء")
        elif score <= -4:
            send_signal_to_telegram("بيع")
        else:
            send_signal_to_telegram("جاري التحليل")

        driver.quit()

    except Exception as e:
        logging.error(f"خطأ في التحليل: {e}")
        send_signal_to_telegram("جاري التحليل")

# تكرار التحليل كل دقيقة
def run_bot():
    while True:
        analyze_market()
        time.sleep(60)

if __name__ == "__main__":
    run_bot()

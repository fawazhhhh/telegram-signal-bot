import time
import logging
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
import pytesseract
import io
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# إعدادات تليجرام
TELEGRAM_BOT_TOKEN = '7803079502:AAE967yp04T8Gy5z66Xd8hwQsi9XfZcVcyk'
CHAT_ID = '7890943736'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# إنشاء المتصفح المتوافق مع سيرفر Render
def create_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# إرسال الإشارة
def send_signal_to_telegram(signal):
    try:
        bot.send_message(CHAT_ID, signal)
    except Exception as e:
        logging.error(f"فشل في إرسال الإشارة: {e}")

# تسجيل الدخول والدخول إلى سوق سمارت
def login_and_navigate(driver):
    driver.get("https://app.expertoption.com/")
    time.sleep(5)

    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    email_input.send_keys("dasf16154@gmail.com")
    password_input.send_keys("AaSs110099")
    password_input.send_keys(Keys.ENTER)

    time.sleep(10)
    driver.get("https://app.expertoption.com/trading/SMART")
    time.sleep(10)

# قراءة الشاشة (OCR)
def read_indicators_with_ocr(driver):
    screenshot = driver.get_screenshot_as_png()
    image = Image.open(io.BytesIO(screenshot))
    text = pytesseract.image_to_string(image, lang='eng+ara')
    return text.lower()

# تحليل السوق
def analyze_market():
    try:
        driver = create_driver()
        login_and_navigate(driver)
        raw_text = read_indicators_with_ocr(driver)

        score = 0

        if "rsi" in raw_text:
            if "30" in raw_text or "25" in raw_text:
                score += 1
            elif "70" in raw_text or "75" in raw_text:
                score -= 1

        if "macd" in raw_text:
            if "صاعد" in raw_text or "up" in raw_text:
                score += 1
            elif "نازل" in raw_text or "down" in raw_text:
                score -= 1

        if "ema" in raw_text:
            if "فوق" in raw_text or "above" in raw_text:
                score += 1
            elif "تحت" in raw_text or "below" in raw_text:
                score -= 1

        if "momentum" in raw_text:
            if "+0" in raw_text or "+1" in raw_text:
                score += 1
            elif "-0" in raw_text or "-1" in raw_text:
                score -= 1

        if any(pattern in raw_text for pattern in ["hammer", "doji", "engulfing"]):
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

# التشغيل المتكرر
def run_bot():
    while True:
        analyze_market()
        time.sleep(60)

if __name__ == "__main__":
    run_bot()

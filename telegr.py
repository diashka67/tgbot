import csv
import requests
from io import StringIO
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from secret import secrets

# ==== НАСТРОЙКИ ====
TELEGRAM_TOKEN = secrets['BOT_API_TOKEN']
CITY = "Minsk"  # Город для прогноза

# ==== ФУНКЦИИ ДЛЯ API ====
def get_weather():
    # Бесплатный API wttr.in
    url = f"https://wttr.in/{CITY}?format=j1"
    r = requests.get(url).json()
    forecast = []
    for day in r["weather"]:
        date = day["date"]
        avgtemp = day["avgtempC"]
        desc = day["hourly"][4]["weatherDesc"][0]["value"]
        forecast.append(f"{date}: {avgtemp}°C, {desc}")
    return "\n".join(forecast)


def get_stock_price():
    # Пример: MSFT.US — Microsoft, AAPL.US — Apple
    ticker = "MSFT.US"
    url = f"https://stooq.com/q/l/?s={ticker}&f=sd2t2ohlcv&h&e=csv"
    r = requests.get(url)
    r.encoding = "utf-8"
    data = list(csv.DictReader(StringIO(r.text)))
    if data and "Close" in data[0]:
        price = data[0]["Close"]
        return f"Цена акции {ticker}: {price} USD"
    else:
        return "Не удалось получить данные по акции."

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    r = requests.get(url).json()
    price = r["bitcoin"]["usd"]
    return f"Bitcoin: {price} USD"

# ==== ОБРАБОТЧИКИ ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Погода", "Акции", "Валюта"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == "погода":
        await update.message.reply_text(get_weather())
    elif text == "акции":
        await update.message.reply_text(get_stock_price())
    elif text == "валюта":
        await update.message.reply_text(get_btc_price())
    else:
        await update.message.reply_text("Не понял команду. Выберите из меню.")

# ==== ЗАПУСК ====
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

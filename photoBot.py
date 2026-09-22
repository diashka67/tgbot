import logging
import csv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from datetime import datetime
from pathlib import Path
import aiohttp
from secret import secrets

TELEGRAM_TOKEN = secrets['BOT_API_TOKEN']
Log_file = Path("bot_log.csv")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def log_file():
    if not Log_file.exists():
        with open(Log_file, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter="\t").writerow(
                ["Uniс_ID", "@TG_nick", "Motion", "API", "Date", "Time", "API_answer"]
            )


def log_action(user, motion: str, api: str = "NONE", api_answer: str = "NONE"):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    user_id = user.id
    username = f"@{user.username}" if user.username else "NONE"
    with open(Log_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow([user_id, username, motion, api, date_str, time_str, api_answer])

    log_line = f"{user_id}\t{username}\t{motion}\t{api}\t{date_str}\t{time_str}\t{api_answer}"
    logger.info(f"LOG: {log_line}")
    print(log_line)


def main_menu():
    keyboard = [
        [InlineKeyboardButton("Погода", callback_data="api:weather")],
        [InlineKeyboardButton("Мой адрес айпишки", callback_data="api:country")],
        [InlineKeyboardButton("Пэс патрон", callback_data="api:dog")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    log_action(user, "/start")

    text = (
        "Приветик!\n\n"
        "Я крутой бот с API:\n"
        "• Погода (Open-Meteo)\n"
        "• Мой IP (ipify)\n"
        "• Пэс патрон (Dog CEO)\n\n"
        "Выбери кнопку или напиши текст."
    )
    await update.message.reply_text(text, reply_markup=main_menu())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    data = query.data

    if data == "api:weather":
        await get_weather(query, user)
    elif data == "api:country":
        await get_country(query, user)
    elif data == "api:dog":
        await get_dog(query, user)
    else:
        await query.message.reply_text("Такой кнопки нет", reply_markup=main_menu())


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    log_action(user, "Keyboard typing")
    await update.message.reply_text(
        f'Вы написали «{text}», я не знаю такой команды',
        reply_markup=main_menu()
    )


async def get_weather(query, user):
    api_name = "Open-Meteo"
    url = "https://api.open-meteo.com/v1/forecast?latitude=53.90&longitude=27.57&current_weather=true"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        weather = data["current_weather"]
        pogoda = (
            f"Погода в Минске:\n"
            f"Температура: {weather['temperature']}°C\n"
            f"Ветер: {weather['windspeed']} км/ч"
        )
        await query.message.reply_text(pogoda, reply_markup=main_menu())
        log_action(user, "Button: Погода", api_name, pogoda)

    except Exception as e:
        error = f"Ошибка API: {e}"
        await query.message.reply_text(error, reply_markup=main_menu())
        log_action(user, "Button: Погода", api_name, error)


async def get_country(query, user):
    api_name = "ipify"
    url = "https://api.ipify.org?format=json"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        ip = data.get("ip", "неизвестно")
        answer = f"Твой IP-адрес: {ip}"

        await query.message.reply_text(answer, reply_markup=main_menu())
        log_action(user, "Button: Мой IP", api_name, answer)

    except Exception as e:
        error = f"Ошибка API: {e}"
        await query.message.reply_text(error, reply_markup=main_menu())
        log_action(user, "Button: Мой IP", api_name, error)


async def get_dog(query, user):
    api_name = "Dog CEO"
    url = "https://dog.ceo/api/breeds/image/random"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        image_url = data["message"]
        await query.message.reply_photo(
            photo=image_url,
            caption="Случайный пэс",
            reply_markup=main_menu()
        )
        log_action(user, "Button: Собака", api_name, image_url)

    except Exception as e:
        error_msg = f"Ошибка API: {e}"
        await query.message.reply_text(error_msg, reply_markup=main_menu())
        log_action(user, "Button: Собака", api_name, error_msg)


def main():
    log_file()
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Бот запущен. Логи → bot_log.csv")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

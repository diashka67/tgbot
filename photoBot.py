import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from secret import secrets
TELEGRAM_TOKEN = secrets['BOT_API_TOKEN']

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
    )
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.full_name}) нажал старт")
    
    await update.message.reply_text(
        "Сап бро! 🤑\n\n"
        "• /send — отправлю тебе картинку\n"
        "• /send_url — отправлю картинку по ссылке"
    )
    
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = r"C:\Users\HONOR\Pictures\5253647552190552837_121.jpg"
    
    try:
        with open(photo_path, "rb") as photo:
            await update.message.reply_photo(
                photo = photo,
                caption = "тупа мы"
            )
            logger.info("Фото успешно отправлено")
    except FileNotFoundError:
        await update.message.reply_text("Файл не найден")
        
async def send_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://i.pinimg.com/736x/c3/e6/69/c3e669f67c6ca042ebffd9b177fdd330.jpg"
    await update.message.reply_photo(
        photo = url,
        caption = "с ссылочки"
    )
    logger.info("чипитосик")
    
    
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    print("Бот создан успешно")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("send", send_photo))
    app.add_handler(CommandHandler("send_url", send_url))
    
    logger.info("Бот запускается...")
    print("Бот запущен")
    app.run_polling(allowed_updates = Update.ALL_TYPES)
    
if __name__ == "__main__":
    main()

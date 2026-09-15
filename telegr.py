import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
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
    logger.info(f"Пользователь {user.id} ({user.full_name}) нажал /start")

    keyboard = [
        [KeyboardButton("Аудио"), KeyboardButton("Видео")],
        [KeyboardButton("Фото"), KeyboardButton("Документ")],
    ]
    
    markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    text = (
        "Сап бро! 🐷\n\n"
        "Выбери кнопку или используй команды:\n"
        "/start — показать кнопки\n"
        "/photo — отправить фото\n"
        "/url_photo — фото по ссылке\n"
        "/video — отправить видео\n"
        "/doc — отправить документ"
    )

    await update.message.reply_text(text, reply_markup=markup)
    
async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = r"C:\Users\HONOR\Pictures\cfff9f55b257ed8a4e5aec82ebde84ec.jpg"
    
    try:
        with open(photo_path, "rb") as photo:
            await update.message.reply_photo(
                photo = photo,
                caption = "тупа ты"
            )
            logger.info("Фото успешно отправлено")
    except FileNotFoundError:
        await update.message.reply_text("Файл не найден")
        
async def send_url_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://i.pinimg.com/736x/c3/e6/69/c3e669f67c6ca042ebffd9b177fdd330.jpg"
    await update.message.reply_photo(
        photo = url,
        caption = "с ссылочки"
    )
    
    logger.info("чипитосик")
async def send_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_audio(audio=f"https://cdn9.sefon.pro/prev/51FILviKqQsjebMWP1mr7g/1789151159/1056/Jambul%20-%20%D0%A4%D1%80%D0%B0%D0%BD%D0%BA%D0%BB%D0%B8%D0%BD%20%28192kbps%29.mp3", 
                                    caption="некий трек", 
                                    title="название", 
                                    performer="артист")
async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_video(
        video="https://www.w3schools.com/html/mov_bbb.mp4",   
        caption="Какое-то видео",
        supports_streaming=True)
    
async def send_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_document(
        document=r"C:\доки\алгебра шпоры экз.pdf",  
        caption="Вот документ"
    )
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Аудио":
        await send_audio(update, context)
    elif text == "Видео":
        await send_video(update, context)
    elif text == "Фото":
        await send_photo(update, context)
    elif text == "Документ":
        await send_document(update, context)
    elif text == "Ссылка на фото":
        await send_url_photo(update, context)
    else:
        await update.message.reply_text("я не понял")
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    print("Бот создан успешно")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("photo", send_photo))
    app.add_handler(CommandHandler("url_photo", send_url_photo))
    app.add_handler(CommandHandler("video", send_video))
    app.add_handler(CommandHandler("doc", send_document))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    logger.info("Бот запускается...")
    print("Бот запущен")
    app.run_polling(allowed_updates = Update.ALL_TYPES)
    
if __name__ == "__main__":
    main()

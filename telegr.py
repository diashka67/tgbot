
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from secret import secrets
TELEGRAM_TOKEN = secrets['BOT_API_TOKEN']

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main_menu():
    keyboard = [
        [InlineKeyboardButton("Аудио", callback_data="media:audio")],
        [InlineKeyboardButton("Видео", callback_data="media:video")],
        [InlineKeyboardButton("Фото", callback_data="media:photo")],
        [InlineKeyboardButton("Фото по ссылке", callback_data="media:url_photo")],
        [InlineKeyboardButton("Документ", callback_data="media:document")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.full_name}) нажал /start")

    text = (
        "Сап бро!\n\n"
        "Выбери кнопку или используй команды:\n"
        "/start — показать кнопки\n"
        "/photo — отправить фото\n"
        "/url_photo — фото по ссылке\n"
        "/video — отправить видео\n"
        "/doc — отправить документ"
    )

    await update.message.reply_text(text, reply_markup=main_menu())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "media:audio":
        await send_audio(query)
    elif data == "media:video":
        await send_video(query)
    elif data == "media:photo":
        await send_photo(query)
    elif data == "media:document":
        await send_document(query)
    elif data == "media:url_photo":
        await send_url_photo(query)
    else:
        await query.message.reply_text("Я не понял")


async def send_photo(source):
    photo_path = r"C:\Users\HONOR\Pictures\cfff9f55b257ed8a4e5aec82ebde84ec.jpg"
    message = source.message if hasattr(source, "message") else source

    try:
        with open(photo_path, "rb") as photo:
            await message.reply_photo(photo=photo, caption="тупа ты")
            logger.info("Фото успешно отправлено")
    except FileNotFoundError:
        await message.reply_text("Файл не найден")


async def send_url_photo(source):
    message = source.message if hasattr(source, "message") else source
    url = "https://i.pinimg.com/736x/c3/e6/69/c3e669f67c6ca042ebffd9b177fdd330.jpg"

    await message.reply_photo(photo=url, caption="с ссылочки")
    logger.info("чипитосик")


async def send_audio(source):
    message = source.message if hasattr(source, "message") else source

    await message.reply_audio(
        audio="https://cdn9.sefon.pro/prev/51FILviKqQsjebMWP1mr7g/1789151159/1056/Jambul%20-%20%D0%A4%D1%80%D0%B0%D0%BD%D0%BA%D0%BB%D0%B8%D0%BD%20%28192kbps%29.mp3",
        caption="некий трек",
        title="название",
        performer="артист"
    )


async def send_video(source):
    message = source.message if hasattr(source, "message") else source

    await message.reply_video(
        video="https://www.w3schools.com/html/mov_bbb.mp4",
        caption="Какое-то видео",
        supports_streaming=True
    )


async def send_document(source):
    message = source.message if hasattr(source, "message") else source
    document_path = r"C:\доки\алгебра шпоры экз.pdf"

    try:
        with open(document_path, "rb") as doc:
            await message.reply_document(document=doc, caption="Вот документ")
    except FileNotFoundError:
        await message.reply_text("Документ не найден")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    print("Бот создан успешно")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("photo", send_photo))
    app.add_handler(CommandHandler("url_photo", send_url_photo))
    app.add_handler(CommandHandler("video", send_video))
    app.add_handler(CommandHandler("doc", send_document))

    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Бот запускается...")
    print("Бот запущен")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

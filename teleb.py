import telebot
from telebot import types

from secret import secrets


# ==== НАСТРОЙКИ ====
TELEGRAM_TOKEN = secrets['BOT_API_TOKEN']

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    info = types.KeyboardButton("Инфо")
    stat = types.KeyboardButton("Статистика")
    keyboard_markup.add(info, stat)
    bot.send_message(message.chat.id, "Привет! Я простой бот на telebot", reply_markup = keyboard_markup)

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "Инфо":
        print(f"Юзверь нажал кнопку {message.text}")
        bot.send_message(message.chat.id, f"Ты нажал кнопку 'Инфо'")
        print("Юзверь получил от меня сообщение о нажатии кнопки")
        with open("images\info.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo)
        print("Юзверь получил картинку")
    elif message.text == "Статистика":
        print(f"Юзверь нажал кнопку {message.text}")
        bot.send_message(message.chat.id, f"Ты нажал кнопку 'Статистика'")
        bot.send_photo(message.chat.id, "https://edinstvo.by/wp-content/uploads/2025/08/197459_64f3d7c2d9f5cc5e18b198572960-1068x645.jpg")# bot.send_sticker(message.chat.id, '') # не уверен
    else:
        print(f"Юзверь нажал кнопку {message.text}")
        #bot.send_message(message.chat.id, f"Ты написал: {message.text}")
        bot.reply_to( message,
        f"Вот file_id этого стикера:\n`{message.sticker.file_id}`",
        parse_mode="Markdown"
        )

# ==== ЗАПУСК ====
def main():
    try:
        print("Бот успешно запущен")
        bot.polling(none_stop=True)
    except:
        print("Бот не смог стартовать")

        

if __name__ == "__main__":
    main()

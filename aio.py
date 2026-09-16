import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from telethon import events, TelegramClient
from datetime import datetime, timedelta
from secret import secrets


# ==== НАСТРОЙКИ ====
TELEGRAM_TOKEN = secrets['BOT_API_TOKEN']
API_ID = secrets['API_ID']
API_TOKEN = secrets['API_TOKEN']
name_session = "first"
targets = [-1001007302005, "@Wylsared"]
chat_admin = 207749386
client = TelegramClient(name_session, API_ID, API_TOKEN)


#функция сборщик на части
@client.on(events.NewMessage(chats = targets))
async def all(event):
    await client.start()
    print("запущено успешно")
    a = await client.get_entity(-1001007302005)
    async for msg in client.iter_messages(a, limit=10):
        if 'iphone' in event.text.lower(): 
            await msg.forward_to(chat_admin)
            print('соо получено из чата:', msg.chat.title)
            print(msg.text)








# Создаём экземпляры бота и диспетчера
'''bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я простой бот на aiogram")

# Обработчик любого текстового сообщения
@dp.message()
async def echo(message: types.Sticker):
    await message.answer(f"Ты написал: {message.sticker.file_id}")'''

# ==== ЗАПУСК ====
async def main():
   
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(all())

import logging
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import asyncio
import json

API_TOKEN = 'Ваш токен'
CHANNEL_ID = 'Айди канала можно узнать через https://t.me/my_id_bot'
IMAGE_IDS_FILE = 'image_ids.json'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправьте мне изображение, и я сохраню его.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def save_image(message: types.Message):
    file_id = message.photo[-1].file_id
    try:
        with open(IMAGE_IDS_FILE, 'r') as file:
            image_ids = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        image_ids = []
    image_ids.append(file_id)
    with open(IMAGE_IDS_FILE, 'w') as file:
        json.dump(image_ids, file)
    await message.reply("Изображение сохранено!")

async def send_images():
    try:
        with open(IMAGE_IDS_FILE, 'r') as file:
            image_ids = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        image_ids = []
    if image_ids:
        image_id = image_ids.pop(0)
        await bot.send_photo(CHANNEL_ID, image_id)
        with open(IMAGE_IDS_FILE, 'w') as file:
            json.dump(image_ids, file)

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_images, 'interval', hours=3)
    scheduler.start()

    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

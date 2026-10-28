import asyncio
import sys

# Принудительная инициализация цикла событий для работы в Python 3.14
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

async def generate_session():
    # Настраиваем полную эмуляцию реального мобильного устройства (Device Spoofing)
    app = Client(
        name="analyst_userbot",
        api_id=int(api_id),
        api_hash=api_hash,
        workdir="src",
        app_version="10.5.3",
        device_model="Samsung Galaxy S24 Ultra",
        system_version="Android 14",
        lang_code="ru"
    )
    
    print("Инициализация безопасного сетевого контура...")
    await asyncio.sleep(2.0) # Задержка для сброса флуд-маркеров провайдера
    
    print("Запуск процесса авторизации...")
    async with app:
        me = await app.get_me()
        print(f"\nАвторизация успешна! Аккаунт: {me.first_name} (@{me.username})")

if __name__ == "__main__":
    loop.run_until_complete(generate_session())

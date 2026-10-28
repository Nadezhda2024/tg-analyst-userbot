import os
import asyncio
import sys
from pyrogram import Client
from dotenv import load_dotenv
from bot.handlers import register_handlers

load_dotenv()

app = Client(
    name="analyst_userbot",
    api_id=int(os.getenv("API_ID", 0)),
    api_hash=os.getenv("API_HASH"),
    workdir="src",
    app_version="10.5.3",
    device_model="Samsung Galaxy S24 Ultra",
    system_version="Android 14",
    lang_code="ru"
)

async def main():
    # Регистрируем сквозные обработчики сбора и анализа данных
    await register_handlers(app)
    
    print("Инициализация клиента...")
    await app.start()
    print("Юзербот успешно запущен в асинхронном режиме и слушает команду .summary.")
    
    from pyrogram import idle
    await idle()
    
    await app.stop()

if __name__ == "__main__":
    # Безопасный паттерн запуска для Python 3.14+, исключающий конфликты циклов событий
    try:
        running_loop = asyncio.get_running_loop()
    except RuntimeError:
        running_loop = None

    if running_loop and running_loop.is_running():
        # Если скрипт вызван внутри запущенного event loop (например, из Jupyter Notebook)
        task = running_loop.create_task(main())
        print("[JUPYTER] Асинхронная задача юзербота успешно делегирована текущему циклу блокнота.")
    else:
        # Если скрипт запущен стандартно напрямую через консоль PowerShell
        asyncio.run(main())

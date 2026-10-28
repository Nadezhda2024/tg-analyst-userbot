import asyncio
import sys
import os

# Принудительно создаем event loop в главном потоке для совместимости с Python 3.14+
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Фиксируем путь к папке src, чтобы импорты 'bot.handlers' работали из любой точки запуска
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Безопасный импорт библиотек и внутренних модулей проекта
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

async def start_bot():
    # Регистрируем сквозные обработчики сбора и анализа данных
    await register_handlers(app)
    
    print("Инициализация клиента...")
    await app.start()
    print("Юзербот успешно запущен в асинхронном режиме и слушает команду .summary.")
    
    from pyrogram import idle
    await idle()
    
    await app.stop()

if __name__ == "__main__":
    loop.run_until_complete(start_bot())

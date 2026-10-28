import os
from pyrogram import Client, filters
from pyrogram.types import Message
from models.ollama_client import OllamaAnalyst

DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "..", "temp_downloads")
# Инициализируем аналитический модуль Ollama
analyst = OllamaAnalyst(model_name="deepseek-r1:1.5b")

async def register_handlers(app: Client):
    
    @app.on_message(filters.me & filters.command("summary", prefixes="."))
    async def handle_summary_command(client: Client, message: Message):
        await message.edit_text("⏳ **Сбор данных и анализ контекста чата...**")
        
        chat_id = message.chat.id
        messages_text = []
        screenshot_path = None
        
        try:
            # 1. Извлекаем последние 50 сообщений для глубокого бизнес-анализа
            async for msg in client.get_chat_history(chat_id, limit=50):
                if msg.id == message.id:
                    continue
                    
                text_content = msg.text or msg.caption
                if text_content:
                    author = msg.from_user.first_name if msg.from_user else "Система"
                    messages_text.append(f"{author}: {text_content}")
                    
                # 2. Перехватываем только самый последний актуальный скриншот
                if not screenshot_path:
                    if msg.photo or (msg.document and msg.document.mime_type and "image" in msg.document.mime_type):
                        if not os.path.exists(DOWNLOADS_DIR):
                            os.makedirs(DOWNLOADS_DIR)
                        
                        screenshot_path = await client.download_media(
                            msg,
                            file_name=os.path.join(DOWNLOADS_DIR, f"screenshot_{msg.id}.jpg")
                        )
            
            messages_text.reverse()
            chat_context = "\n".join(messages_text)
            
            await message.edit_text("🤖 **Генерация саммари моделью DeepSeek-R1...**")
            
            # 3. Передаем собранные данные в локальную модель Ollama
            summary_result = await analyst.generate_summary(chat_context, image_path=screenshot_path)
            
            # 4. Выводим готовое краткое саммари для аналитика прямо в чат Telegram
            await message.edit_text(summary_result)
            
        except Exception as e:
            await message.edit_text(f"❌ **Произошла ошибка в пайплайне аналитики:** {str(e)}")
            
        finally:
            # 5. Паттерн автоочистки: жестко удаляем медиафайл с диска, чтобы не засорять память
            if screenshot_path and os.path.exists(screenshot_path):
                try:
                    os.remove(screenshot_path)
                    print(f"[INFO] Временный скриншот успешно удален из хранилища: {screenshot_path}")
                except Exception as cache_error:
                    print(f"[ERROR] Не удалось удалить временный файл: {cache_error}")

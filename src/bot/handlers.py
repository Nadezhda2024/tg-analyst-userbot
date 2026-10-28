from pyrogram import Client, filters
from pyrogram.types import Message
from models.ollama_client import OllamaAnalyst

analyst = OllamaAnalyst(model_name="deepseek-r1:1.5b")

async def register_handlers(app: Client):
    
    @app.on_message(filters.me & filters.command("summary", prefixes="."))
    async def handle_summary_command(client: Client, message: Message):
        chat_id = message.chat.id
        chat_title = message.chat.title or "Личный диалог"
        messages_text = []
        has_screenshot = False
        
        # 1. Сразу удаляем команду из рабочего чата
        await message.delete()
        
        # 2. Создаем лог-уведомление в Избранном
        status_message = await client.send_message(
            "me", 
            f"⏳ **Начат скрытый анализ чата «{chat_title}»...**"
        )
        
        try:
            # 3. Собираем только текстовые логи
            async for msg in client.get_chat_history(chat_id, limit=50):
                text_content = msg.text or msg.caption
                if text_content:
                    author = msg.from_user.first_name if msg.from_user else "Система"
                    messages_text.append(f"{author}: {text_content}")
                    
                # Фиксируем факт наличия медиа в истории переписки без скачивания на диск
                if not has_screenshot:
                    if msg.photo or (msg.document and msg.document.mime_type and "image" in msg.document.mime_type):
                        has_screenshot = True
            
            messages_text.reverse()
            chat_context = "\n".join(messages_text)
            
            await status_message.edit_text(f"🤖 **Контекст чата «{chat_title}» собран. DeepSeek-R1 генерирует саммари...**")
            
            # 4. Передаем аргументы последовательно во избежание конфликта имен переменных
            summary_result = await analyst.generate_summary(chat_context, has_screenshot)
            
            # 5. Выводим готовый отчет
            final_report = f"📋 **Саммари чата: {chat_title}**\n\n{summary_result}"
            await status_message.edit_text(final_report)
            
        except Exception as e:
            await status_message.edit_text(f"❌ **Ошибка аналитики чата «{chat_title}»:** {str(e)}")

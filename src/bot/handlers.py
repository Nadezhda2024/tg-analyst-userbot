from pyrogram import Client, filters
from pyrogram.types import Message
from models.yandex_client import YandexAnalyst

analyst = YandexAnalyst()

async def register_handlers(app: Client):
    
    @app.on_message(filters.me & filters.command("summary", prefixes="."))
    async def handle_summary_command(client: Client, message: Message):
        chat_id = message.chat.id
        chat_title = message.chat.title or "Личный диалог"
        messages_text = []
        
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
                    
            messages_text.reverse()
            chat_context = "\n".join(messages_text)
            
            await status_message.edit_text(f"🤖 **Контекст чата «{chat_title}» собран. Yandex AI Studio генерирует саммари...**")
            
            summary_result = await analyst.generate_summary(chat_context)
            
            # 5. Выводим готовый отчет
            final_report = f"📋 **Саммари чата: {chat_title}**\n\n{summary_result}"
            await status_message.edit_text(final_report)
            
        except Exception as e:
            await status_message.edit_text(f"❌ **Ошибка аналитики чата «{chat_title}»:** {str(e)}")

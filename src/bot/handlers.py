import traceback

from pyrogram import Client, filters
from pyrogram.types import Message
from models.ollama_client import OllamaAnalyst
from models.yandex_client import YandexAnalyst

local_analyst = OllamaAnalyst(model_name="qwen2.5:3b")
api_analyst = YandexAnalyst()

async def register_handlers(app: Client):

    async def summarize_chat(
        client: Client,
        message: Message,
        analyst: OllamaAnalyst | YandexAnalyst,
        provider_label: str,
    ) -> None:
        chat_id = message.chat.id
        chat_title = message.chat.title or "Личный диалог"
        messages_text = []

        await message.delete()
        status_message = await client.send_message(
            "me",
            f"⏳ **Начат скрытый анализ чата «{chat_title}»...**"
        )

        try:
            async for msg in client.get_chat_history(chat_id, limit=50):
                text_content = msg.text or msg.caption
                if text_content:
                    author = msg.from_user.first_name if msg.from_user else "Система"
                    messages_text.append(f"{author}: {text_content}")

            messages_text.reverse()
            chat_context = "\n".join(messages_text)

            await status_message.edit_text(
                f"🤖 **Контекст чата «{chat_title}» собран. "
                f"{provider_label} генерирует саммари...**"
            )
            summary_result = await analyst.generate_summary(chat_context)

            final_report = (
                f"📋 **[{provider_label}] Саммари чата: {chat_title}**\n\n"
                f"{summary_result}"
            )
            await status_message.edit_text(final_report)
        except Exception as e:
            error_msg = f"❌ **Ошибка аналитики:** {str(e)}\n\n```powershell\n{traceback.format_exc()}```"
            await status_message.edit_text(error_msg)

    @app.on_message(filters.me & filters.command("summary", prefixes="."))
    async def handle_local_summary(client: Client, message: Message) -> None:
        await summarize_chat(client, message, local_analyst, "Локальный ИИ")

    @app.on_message(filters.me & filters.command("summary_api", prefixes="."))
    async def handle_api_summary(client: Client, message: Message) -> None:
        await summarize_chat(client, message, api_analyst, "Облачный API")

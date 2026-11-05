import re

import httpx


class OllamaAnalyst:
    def __init__(self, model_name: str = "qwen2.5:3b"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/chat"

    async def generate_summary(self, chat_context: str) -> str:
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ты — строгий аналитик рабочих переписок. Твоя задача — извлечь "
                        "из лога только факты, относящиеся к делам, проектам и задачам. "
                        "Полностью игнорируй бытовой шум: приветствия, разговоры о "
                        "здоровье, погоде, еде, парковках, собаках и обсуждение работы "
                        "самого бота.\n\n"
                        "Сформулируй ответ строго по схеме:\n"
                        "### Тема\n"
                        "Кратко назови ключевое деловое обсуждение (1-2 предложения).\n\n"
                        "### Решения и действия\n"
                        "Перечисли только принятые договоренности. Запрещено дублировать "
                        "мысли или писать одинаковые пункты. Пиши кратко.\n\n"
                        "### Задачи\n"
                        "Конкретные шаги: КТО и ЧТО должен сделать. Не придумывай задачи "
                        "из бытовых диалогов.\n\n"
                        "### Открытые вопросы\n"
                        "Только критические рабочие моменты, оставшиеся без ответа. Не "
                        "задавай бессмысленных вопросов к бытовому контексту.\n\n"
                        "Важное правило: Пиши только правду на основе текста лога. Никогда "
                        "не дублируй пункты в списках."
                    ),
                },
                {
                    "role": "user",
                    "content": f"ЛОГ ПЕРЕПИСКИ:\n\n{chat_context}",
                },
            ],
            "options": {"temperature": 0.2},
            "stream": False,
        }

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(self.api_url, json=payload)

        response.raise_for_status()
        try:
            result = response.json()
            content = result["message"]["content"]
        except (ValueError, KeyError, TypeError) as exc:
            raise RuntimeError("Ollama вернула ответ без ожидаемого текста.") from exc

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Ollama вернула пустой текст.")

        summary = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        if not summary:
            summary = content.replace("<think>", "").replace("</think>", "").strip()

        return summary
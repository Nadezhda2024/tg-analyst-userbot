import os
import re
from ollama import AsyncClient

class OllamaAnalyst:
    def __init__(self, model_name: str = "deepseek-r1:1.5b"):
        self.model_name = model_name
        self.client = AsyncClient()

    def _clean_think_tags(self, text: str) -> str:
        return re.sub(re.compile(r'<think>.*?</think>', re.DOTALL), '', text).strip()

    async def generate_summary(self, chat_context: str, has_screenshot: bool = False) -> str:
        system_prompt = (
            "Ты — профессиональный системный и бизнес-аналитик. "
            "Проанализируй предоставленный контекст переписки. "
            "Сделай короткое, структурированное саммари. Выдели ключевые требования, "
            "задачи, проблемы и договоренности. Пиши строго по делу, техническим языком."
        )
        
        media_marker = "\n(Примечание: К данной переписке участниками был прикреплен рабочий скриншот/изображение)\n" if has_screenshot else ""
        prompt = f"Контекст переписки для анализа:{media_marker}\n\n{chat_context}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        try:
            response = await self.client.chat(
                model=self.model_name,
                messages=messages
            )
            raw_content = response['message']['content']
            return self._clean_think_tags(raw_content)
        except Exception as e:
            return f"Ошибка при обращении к локальной модели Ollama: {str(e)}"

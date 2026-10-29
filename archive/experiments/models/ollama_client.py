import re
import httpx

class OllamaAnalyst:
    def __init__(self, model_name: str = "deepseek-r1:1.5b"):
        self.model_name = model_name
        # Локальный URL сервера Ollama API
        self.api_url = "http://localhost:11434/api/chat"

    def _clean_think_tags(self, text: str) -> str:
        # 1. Пробуем вырезать теги размышлений
        cleaned = re.sub(re.compile(r'<think>.*?</think>', re.DOTALL), '', text).strip()
        
        # 2. Предохранитель: если модель спрятала весь ответ внутрь think, просто удаляем сами теги
        if not cleaned and text:
            cleaned = text.replace("<think>", "").replace("</think>", "").strip()
        return cleaned

    async def generate_summary(self, chat_context: str, has_screenshot: bool = False) -> str:
        # Моно-промпт: все инструкции и данные объединяем в один блок для стабильности модели 1.5b
        calibrated_prompt = (
            "Ты — аналитик данных. Твоя задача — прочитать лог переписки и сделать очень краткое саммари.\n"
            "ПРАВИЛО: Пиши только на понятном русском языке. Не выдумывай факты, которых нет в тексте.\n\n"
            f"ЛОГ ПЕРЕПИСКИ ДЛЯ АНАЛИЗА:\n\"\"\"\n{chat_context}\n\"\"\"\n\n"
            "Заполни этот шаблон только фактами из текста:\n"
            "📌 **Тема:** (Суть обсуждения)\n"
            "🛠 **Задачи:** (Кто что делает)\n"
            "🤝 **Итог:** (Договоренности)"
        )
        
        # Формируем стандартный JSON-пакет для Ollama API
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": calibrated_prompt}
            ],
            "options": {
                "temperature": 0.4,
                "num_predict": 400
            },
            "stream": False
        }

        try:
            # Настройка trust_env=False принудительно заставляет трафик к Ollama идти в обход VPN
            async with httpx.AsyncClient(trust_env=False) as client:
                response = await client.post(self.api_url, json=payload, timeout=60.0)
                
                if response.status_code == 200:
                    result_json = response.json()
                    raw_content = result_json["message"]["content"]
                    return self._clean_think_tags(raw_content)
                else:
                    return f"Ошибка сервера Ollama (Код {response.status_code}): {response.text}"

                    
        except httpx.TimeoutException:
            return "Ошибка: Локальная модель превысила время ожидания ответа (таймаут 60 сек)."
        except Exception as e:
            return f"Сбой прямого подключения к Ollama API: {str(e)}"

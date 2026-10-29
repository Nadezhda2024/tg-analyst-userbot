import os
import httpx
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "Qwen/Qwen2.5-72B-Instruct"

async def generate_summary(text_content: str) -> str:
    if not HF_TOKEN:
        raise ValueError("Критическая ошибка: HF_TOKEN не найден в переменных окружения.")

    # Исправленный OpenAI-совместимый эндпоинт Serverless Inference API
    url = "https://router.huggingface.co/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": text_content
            }
        ],
        "temperature": 0.2,
        "max_tokens": 1024
    }
    
    async with httpx.AsyncClient(trust_env=False) as client:
        response = await client.post(url, headers=headers, json=payload, timeout=60.0)
        
        if response.status_code != 200:
            raise RuntimeError(f"Ошибка Hugging Face API ({response.status_code}): {response.text}")
            
        result = response.json()
        return result["choices"][0]["message"]["content"]

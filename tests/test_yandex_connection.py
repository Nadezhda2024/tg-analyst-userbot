import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")

api_key = os.getenv("YANDEX_CLOUD_API_KEY")
folder_id = os.getenv("YANDEX_CLOUD_FOLDER") or os.getenv("YANDEX_FOLDER_ID")

if not api_key:
	raise SystemExit("YANDEX_CLOUD_API_KEY не найден в .env.")
if not folder_id:
	raise SystemExit(
		"YANDEX_CLOUD_FOLDER не найден в .env. Укажите ID каталога из Yandex AI Studio."
	)

model = "qwen3.6-35b-a3b/latest"
url = "https://ai.api.cloud.yandex.net/v1/chat/completions"
headers = {
	"Authorization": f"Api-Key {api_key}",
	"Content-Type": "application/json",
}
payload = {
	"model": f"gpt://{folder_id}/{model}",
	"messages": [
		{"role": "system", "content": "Отвечай кратко и по-русски."},
		{"role": "user", "content": "Ответь одним словом: OK"},
	],
	"max_completion_tokens": 256,
	"temperature": 0,
	"reasoning_effort": "none",
}

print(f"Проверяю Yandex AI Studio: {model}")
try:
	response = httpx.post(url, headers=headers, json=payload, timeout=60)
except httpx.RequestError as exc:
	raise SystemExit(f"Не удалось подключиться к Yandex AI Studio: {exc}") from exc

print(f"Статус-код: {response.status_code}")
try:
	result = response.json()
except ValueError:
	result = {}

if not response.is_success:
	error = result.get("error", {}).get("message", response.text)
	print(f"Ошибка API: {str(error).replace(api_key, '[скрыт]')}")
	raise SystemExit(1)

try:
	text = result["choices"][0]["message"]["content"]
except (KeyError, IndexError, TypeError):
	raise SystemExit("API вернул успешный статус, но ответ не содержит ожидаемый текст.")
if not isinstance(text, str) or not text.strip():
	raise SystemExit("API вернул пустой текст. Увеличьте max_completion_tokens или проверьте модель.")

print(f"Ответ модели: {text}")
usage = result.get("usage", {})
if usage:
	print(
		"Токены этого запроса: "
		f"вход {usage.get('prompt_tokens', '?')}, "
		f"выход {usage.get('completion_tokens', '?')}, "
		f"всего {usage.get('total_tokens', '?')}"
	)
print("Подключение и генерация работают.")
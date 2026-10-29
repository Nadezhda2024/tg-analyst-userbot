import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
model = "gemini-3.6-flash"

if not api_key:
	raise SystemExit("GEMINI_API_KEY не найден в .env или переменных окружения.")

url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
payload = {
	"contents": [{"parts": [{"text": "Ответь одним словом: OK"}]}],
	"generationConfig": {"maxOutputTokens": 128},
}

print(f"Проверка подключения к Gemini: {model}")
try:
	response = requests.post(url, headers=headers, json=payload, timeout=30)
except requests.RequestException as exc:
	raise SystemExit(f"Не удалось подключиться к Gemini API: {exc}") from exc

print(f"Статус-код: {response.status_code}")
try:
	result = response.json()
except requests.exceptions.JSONDecodeError:
	result = {}


if response.ok:
	try:
		text = result["candidates"][0]["content"]["parts"][0]["text"]
	except (KeyError, IndexError, TypeError):
		raise SystemExit("Gemini вернул успешный статус, но ответ не содержит ожидаемый текст.")
	print(f"Ответ модели: {text}")
	print("Подключение и генерация работают.")
else:
	error = result.get("error", {}).get("message", response.text)
	print(f"Ошибка API: {str(error).replace(api_key, '[скрыт]')}")
	raise SystemExit(1)

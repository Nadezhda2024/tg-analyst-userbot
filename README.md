# Telegram Data Analyst Userbot
![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Qwen](https://img.shields.io/badge/Qwen-%236950EF.svg?style=for-the-badge&logo=qwen&logoColor=white)
![Ollama](https://img.shields.io/badge/ollama-%23000000.svg?style=for-the-badge&logo=ollama&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![API](https://img.shields.io/badge/-API-FF6600?style=for-the-badge&logo=API)
[![Yandex AI Studio](https://img.shields.io/badge/Yandex-AI%20Studio-yellow?style=flat-square&logo=yandex)](https://cloud.yandex.ru/services/ai-studio)

Асинхронный Telegram userbot для подготовки кратких отчётов по истории чата. Поддерживаются два текстовых режима: локальная Ollama и облачная Yandex AI Studio. Анализ изображений пока не реализован.

## Режимы работы

- `.summary` — анализирует до 50 последних сообщений локальной моделью `qwen2.5:3b` через Ollama. Результат помечается `[Локальный ИИ]`.
- `.summary_api` — анализирует те же текстовые сообщения моделью `qwen3.6-35b-a3b/latest` через Yandex AI Studio. Результат помечается `[Облачный API]`.

Команды доступны владельцу аккаунта. Результат отправляется в «Избранное». Сообщения собираются в хронологическом порядке. Картинки сейчас не скачиваются и не передаются моделям.

## Структура проекта

- `main.py` — запускает Pyrogram-клиент и обработчики.
- `run_bot.vbs` — запускает `main.py` в фоне без консольного окна.
- `src/auth.py` — первичный вход в Telegram и создание локальной сессии.
- `src/bot/handlers.py` — обработка `.summary` и `.summary_api`, сбор истории и отправка результата.
- `src/models/ollama_client.py` — асинхронный клиент локальной Ollama.
- `src/models/yandex_client.py` — клиент Yandex AI Studio.
- `tests/test_yandex_connection.py` — проверка Yandex API на коротком тестовом запросе без запуска Telegram.
- `archive/experiments/` — старые ноутбуки, промпты, заметки и неиспользуемые клиенты.
- `.env` — локальные секреты: `API_ID`, `API_HASH`, `YANDEX_CLOUD_API_KEY`, `YANDEX_CLOUD_FOLDER`. Файл игнорируется Git.
- `src/analyst_userbot.session*` — локальная авторизованная Telegram-сессия. Не публикуйте и не передавайте её.

## Первичная настройка

1. Создайте виртуальное окружение и установите зависимости `pyrogram`, `httpx`, `python-dotenv`.
2. Установите и запустите Ollama, скачайте модель командой `ollama run qwen2.5:3b`.
3. Заполните локальный `.env` значениями `API_ID`, `API_HASH`, `YANDEX_CLOUD_API_KEY` и `YANDEX_CLOUD_FOLDER`. Не добавляйте реальные ключи в README или Git.
4. При первом входе включите VPN и запустите в терминале `python .\src\auth.py`. Введите код и пароль Telegram непосредственно в терминале. Эта авторизация выполняется один раз; после отзыва сессии её нужно создать заново.
5. Проверьте Yandex API без запуска Telegram: `python .\tests\test_yandex_connection.py`.

## Автоматизация фонового запуска

Файл `run_bot.vbs` запускает интерпретатор из локального `venv` и `main.py` в скрытом режиме.

**Перед каждым запуском `run_bot.vbs` VPN на компьютере должен быть включён и подключён. Это обязательно и при ручном запуске файла, и при запуске через автозагрузку Windows в `shell:startup`. Без VPN Pyrogram не сможет установить соединение с Telegram; процесс Python будет продолжать сетевые попытки и получать `Connection timed out`.**

Для ручного запуска подключите VPN и дважды щёлкните `run_bot.vbs`. Для автоматического запуска нажмите `Win+R`, введите `shell:startup` и поместите в открывшуюся папку ярлык на `run_bot.vbs`. Проверьте, что VPN подключён до входа в Windows или до запуска userbot из автозагрузки.

Проверка процесса:

1. Подключите VPN и запустите `run_bot.vbs`.
2. Откройте Диспетчер задач сочетанием `Ctrl+Shift+Esc` и выберите вкладку «Подробности».
3. Найдите `python.exe`. Чтобы отличить userbot от других Python-процессов, щёлкните заголовок списка правой кнопкой, включите столбец «Командная строка» и проверьте, что команда содержит `venv\Scripts\python.exe` и `main.py`.
4. Отправьте `.summary` или `.summary_api` в Telegram и проверьте ответ в «Избранном».
5. Чтобы остановить userbot, завершите только найденный процесс `python.exe`, у которого в командной строке указан путь к этому проекту и `main.py`.

Консольное окно при запуске через VBS не отображается. Для диагностики ошибок обработчик отправляет traceback в статусное сообщение Telegram.

## Умный Справочник (Smart Handbook)

Telegram‑бот и CLI для получения кратких определений и ссылок из Wikipedia.

### Возможности
- **/wiki <термин>**: краткое определение из Wikipedia с возможностью переключения на полный текст
- **Инлайн‑кнопки**:
  - Переключение режима: кратко ⇄ полностью
  - Открыть оригинальную статью в браузере
- Хранение состояния диалога на пользователя (последний термин, режим отображения и т.д.)
- Консольная утилита для быстрого получения определения из терминала

### Структура проекта
```text
smart_handbook/
├─ smart_handbook/
│  ├─ api_clients/
│  │  └─ wikipedia_client.py     # Клиент для Wikipedia API
│  └─ cli/
│     └─ main.py                 # CLI интерфейс
└─ telegram_bot/
   ├─ bot.py                     # Точка входа Telegram‑бота
   ├─ handlers/
   │  ├─ command_handlers.py     # /start, /help, /wiki и вспом. функции
   │  └─ callback_handlers.py    # Обработчики инлайн‑кнопок
   └─ state.py                   # Память о состоянии пользователей
```

### Требования
- Python 3.10+
- Доступ в интернет (для запросов к Wikipedia)

Зависимости указаны в `requirements.txt`

### Установка
```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate    # Windows PowerShell
pip install -r requirements.txt
```

### Настройка окружения
1) Создайте файл `.env` в корне проекта на основе `example.env`:
```env
TG_BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BotFather
```

### Запуск Telegram‑бота
```bash
python -m telegram_bot.bot
```
Если запуск успешен, в консоли появится сообщение «Бот запускается». Откройте диалог с ботом в Telegram и используйте команды ниже.

### Команды бота
- `/start` — приветствие и краткая инструкция
- `/help` — справка и примеры
- `/wiki <термин>` — получить краткое определение. Пример: `/wiki Интеграл`

После `/wiki` бот отправит текст и инлайн‑кнопки:
- «Показать полный» / «Показать кратко» — переключение режима
- «Открыть статью» — переход к оригиналу на Wikipedia (если ссылка найдена)

### CLI (консольная утилита)
```bash
python -m smart_handbook.cli.main "Интеграл" --lang ru
```
Опции:
- `term` — обязательный аргумент (термин)
- `--lang {ru,en}` — язык (по умолчанию `ru`)

### Технические детали
- Хранение состояния: `telegram_bot/state.py` (в памяти процесса)
- Обработчики команд: `telegram_bot/handlers/command_handlers.py`
- Обработчики колбэков: `telegram_bot/handlers/callback_handlers.py`
- Клиент Wikipedia: `smart_handbook/api_clients/wikipedia_client.py`

### Отладка и подсказки
- Нет ответов/ошибки сети: проверьте интернет и доступность `wikipedia.org`
- Токен: убедитесь, что `TG_BOT_TOKEN` корректен и бот не заблокирован
- Длина сообщений Telegram: текст обрезается до безопасного лимита (~3900 символов)


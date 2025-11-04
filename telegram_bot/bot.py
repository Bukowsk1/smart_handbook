import os
from pathlib import Path

import telebot
from dotenv import load_dotenv

from telegram_bot.handlers.command_handlers import register_handlers
from telegram_bot.handlers.callback_handlers import register_callback_handlers


def main() -> None:
    """
    Запускает бота.
    
    TODO:
        1. Загрузи .env файл +
        2. Получи токен из переменной окружения +
        3. Проверь, что токен не пустой
        4. Создай экземпляр бота +
        5. Зарегистрируй обработчики команд
        6. Выведи сообщение о запуске
        7. Запусти бота 
        8. Оберни создание и запуск бота в try/except
    """
    try:
        load_dotenv()
        token = os.getenv("TG_BOT_TOKEN") or os.getenv("WIKI_TOKEN")
        
        if not token:
            raise ValueError("Токен бота не найден в переменных окружения. Убедитесь, что TG_BOT_TOKEN установлен в .env файле.")
        
        bot = telebot.TeleBot(token)
        register_handlers(bot)
        register_callback_handlers(bot)
        print("Бот запускается")
        bot.polling()
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        raise

    


if __name__ == "__main__":
    main()

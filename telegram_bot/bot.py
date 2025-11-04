import os
from pathlib import Path

import telebot
from dotenv import load_dotenv

from telegram_bot.handlers.command_handlers import register_handlers


def main() -> None:
    """
    Запускает бота.
    
    TODO:
        1. Загрузи .env файл
        2. Получи токен из переменной окружения
        3. Проверь, что токен не пустой
        4. Создай экземпляр бота
        5. Зарегистрируй обработчики команд
        6. Выведи сообщение о запуске
        7. Запусти бота
        8. Оберни создание и запуск бота в try/except
    """
    raise NotImplementedError(
        "Реализуй функцию main() согласно заданию"
    )


if __name__ == "__main__":
    main()

import requests
from smart_handbook.api_clients.wikipedia_client import WikipediaClient

# Создаём экземпляр клиента Wikipedia
wikipedia_client = WikipediaClient()


def register_handlers(bot):
    """
    Регистрирует все обработчики команд для бота.
    
    Args:
        bot: Экземпляр telebot.TeleBot
    
    TODO:
        Реализуй все обработчики команд внутри этой функции.
        Используй декораторы @bot.message_handler() для регистрации.
    """
    
    @bot.message_handler(commands=['start'])
    def start_command(message):
        """
        Обработчик команды /start.
        
        TODO:
            Отправь приветственное сообщение с помощью bot.send_message()
            Подскажи пользователю, как использовать бота.
            Пример: "Привет! Я Умный Справочник. Чтобы получить определение, 
                     используйте команду /wiki <термин>. Например: /wiki Интеграл"
        """
        raise NotImplementedError("Реализуй обработчик команды /start")
    
    @bot.message_handler(commands=['help'])
    def help_command(message):
        """
        Обработчик команды /help.
        
        TODO:
            Отправь справку по использованию бота.
            Покажи примеры команд.
            Пример: "Я могу найти краткое определение по любому термину из Wikipedia.
                     Просто используйте команду /wiki <термин>.\nПример: /wiki Эйлер"
        """
        raise NotImplementedError("Реализуй обработчик команды /help")
    
    @bot.message_handler(commands=['wiki'])
    def wiki_command(message):
        """
        Обработчик команды /wiki.
        
        TODO:
            1. Извлеки термин
            2. Если термин не указан:
               - Отправь подсказку: "Пожалуйста, укажите термин для поиска..."
            3. Получи термин
            4. Вызови wikipedia_client.get_summary(term, lang="ru") в блоке try/except:
               - Если summary не None -> отправь его пользователю
               - Если summary == None -> отправь "Термин '{term}' не найден в Wikipedia."
            5. Обработай исключения
        """
        raise NotImplementedError("Реализуй обработчик команды /wiki")
    
    @bot.message_handler(func=lambda message: message.text.startswith('/'))
    def unknown_command(message):
        """
        Обработчик неизвестных команд (любая команда, начинающаяся с /).

        TODO:
            Отправь сообщение: "Неизвестная команда. Используйте /wiki <термин>."
        """
        raise NotImplementedError("Реализуй обработчик неизвестных команд")

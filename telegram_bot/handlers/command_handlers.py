import telebot
from telebot import types
from smart_handbook.api_clients.wikipedia_client import WikipediaClient
from telegram_bot.state import get_user_state, update_user_state
MAX_LEN = 3900  # лимит Telegram ~4096

wikipedia_client = WikipediaClient()


def register_handlers(bot: telebot.TeleBot) -> None:
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
        bot.send_message(
            message.chat.id,
            "Привет! Я Умный Справочник. Чтобы получить определение, "
            "используйте команду /wiki <термин>. Например: /wiki Интеграл"
        )
        
    
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
        bot.send_message(
            message.chat.id,
            "Я могу найти краткое определение по любому термину из Wikipedia. "
            "Просто используйте команду /wiki <термин>.\nПример: /wiki Эйлер"
        )
    
    @bot.message_handler(commands=['wiki'])
    def wiki_command(message):
        """Команда /wiki: отправляет краткое определение + кнопки."""
        parts = message.text.split(' ', 1)
        if len(parts) < 2 or not parts[1].strip():
            bot.send_message(
                message.chat.id,
                "Пожалуйста, укажите термин для поиска. Например: /wiki Интеграл"
            )
            return
        term = parts[1].strip()

        chat_id = message.chat.id
        state = get_user_state(chat_id)

        try:
            summary = wikipedia_client.get_summary(term, lang="ru")
            full_text = wikipedia_client.get_full_article(term, lang="ru")
            article_url = wikipedia_client.get_article_url(term, lang="ru")

            if not summary and not full_text:
                bot.send_message(chat_id, f"Термин '{term}' не найден в Wikipedia.")
                return

            update_user_state(
                chat_id,
                last_term=term,
                display_mode='summary',
                summary_text=_cut(summary),
                full_text=_cut(full_text),
                article_url=article_url,
            )

            current = get_user_state(chat_id)
            text_to_send = current['summary_text'] or current['full_text'] or ""
            sent = bot.send_message(chat_id, text_to_send, reply_markup=_keyboard(current))
            update_user_state(chat_id, last_message_id=sent.message_id)

        except Exception:
            bot.send_message(chat_id, f"Произошла ошибка при поиске термина '{term}'. Попробуйте позже.")
        
    
    @bot.message_handler(func=lambda message: message.text and message.text.startswith('/') and 
                         message.text.split()[0][1:] not in ['start', 'help', 'wiki'])
    def unknown_command(message):
        """
        Обработчик неизвестных команд (любая команда, начинающаяся с /).

        TODO:
            Отправь сообщение: "Неизвестная команда. Используйте /wiki <термин>."
        """
        bot.send_message(
            message.chat.id,
            "Неизвестная команда. Используйте /wiki <термин>."
        )

def _cut(text: str | None) -> str:
    """Обрезает текст до MAX_LEN символов."""
    if not text:
        return ""
    return text if len(text) <= MAX_LEN else text[:MAX_LEN] + "…"

def _keyboard(state: dict) -> types.InlineKeyboardMarkup:
    """Создает клавиатуру с инлайн-кнопками."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    toggle_text = 'Показать полный' if state.get('display_mode') == 'summary' else 'Показать кратко'
    toggle_btn = types.InlineKeyboardButton(text=toggle_text, callback_data='wiki:toggle')
    buttons = [toggle_btn]
    article_url = state.get('article_url')
    if article_url:
        buttons.append(types.InlineKeyboardButton(text='Открыть статью', url=article_url))
    markup.add(*buttons)
    return markup
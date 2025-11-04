from telebot import types

from smart_handbook.api_clients.wikipedia_client import WikipediaClient
from telegram_bot.handlers.command_handlers import _cut, _keyboard
from telegram_bot.state import get_user_state, update_user_state

wikipedia_client = WikipediaClient()


def register_callback_handlers(bot):
    """
    Регистрирует обработчики callback-запросов для бота.
    
    Args:
        bot: Экземпляр telebot.TeleBot
    """
    
    @bot.callback_query_handler(func=lambda call: call.data and call.data.startswith('wiki:'))
    def handle_wiki_callback(call):
        """Обработчик callback-запросов для кнопок Wikipedia."""
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass

        message = call.message
        if not message:
            return
        chat_id = message.chat.id
        message_id = message.message_id
        state = get_user_state(chat_id)

        last_message_id = state.get('last_message_id')
        if last_message_id and last_message_id != message_id:
            return

        data = call.data

        if data == 'wiki:toggle':
            current_mode = state.get('display_mode', 'summary')
            new_mode = 'full' if current_mode == 'summary' else 'summary'
            new_text = _cut(state.get('full_text') if new_mode == 'full' else state.get('summary_text'))

            update_user_state(chat_id, display_mode=new_mode)
            updated_state = get_user_state(chat_id)

            try:
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=new_text or '',
                    reply_markup=_keyboard(updated_state)
                )
            except Exception:
                try:
                    bot.edit_message_reply_markup(
                        chat_id=chat_id,
                        message_id=message_id,
                        reply_markup=_keyboard(updated_state)
                    )
                except Exception:
                    pass
        else:
            return
        
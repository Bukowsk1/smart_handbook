user_states = {}


def get_user_state(chat_id: int) -> dict:
    """
    Получает состояние пользователя. Создает новое, если не существует.
    
    Args:
        chat_id (int): ID чата пользователя
        
    Returns:
        dict: Словарь с состоянием пользователя
    """

    if chat_id not in user_states:
        user_states[chat_id] = {
            'last_term': None,
            'display_mode': 'summary', 
            'summary_text': None,
            'full_text': None,
            'article_url': None,
            'last_message_id': None
        }
    return user_states[chat_id]



def update_user_state(chat_id: int, **kwargs) -> None:
    """
    Обновляет состояние пользователя.
    
    Args:
        chat_id (int): ID чата пользователя
        **kwargs: Параметры для обновления
    """
    state = get_user_state(chat_id)
    state.update(kwargs)


def clear_user_state(chat_id: int) -> None:
    """
    Очищает состояние пользователя.
    
    Args:
        chat_id (int): ID чата пользователя
    """
    user_states.pop(chat_id, None)
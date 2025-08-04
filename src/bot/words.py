from aiogram import Dispatcher, types, F
from database.models import get_user, get_words_by_level, add_learned_word, add_word_to_spaced_repetition
from .config import WORDS_PER_DAY

async def cmd_words(message: types.Message):
    """Обработчик команды /words"""
    user_id = message.from_user.id
    
    # Получаем информацию о пользователе
    user = get_user(user_id)
    
    if not user:
        await message.answer(
            "Сначала нужно выбрать уровень! Напиши /start"
        )
        return
    
    # Получаем слова для уровня пользователя
    words = get_words_by_level(user['level'], WORDS_PER_DAY)
    
    if not words:
        await message.answer(
            f"К сожалению, для уровня {user['level']} пока нет слов в базе данных.\n"
            "Попробуйте другой уровень или обратитесь к администратору."
        )
        return
    
    # Формируем сообщение со словами
    words_text = f"📚 Вот твои {len(words)} слов для изучения:\n\n"
    
    for i, word_data in enumerate(words, 1):
        words_text += (
            f"{i}. **{word_data['word']}** [{word_data['transcription']}]\n"
            f"   Перевод: {word_data['translation']}\n"
            f"   Пример: {word_data['example']}\n\n"
        )
        
        # Добавляем слово в список выученных
        add_learned_word(user_id, word_data['word'])
        
        # Добавляем слово в систему интервального повторения
        add_word_to_spaced_repetition(user_id, word_data['word_id'], word_data['word'])
    
    words_text += (
        "💡 Эти слова добавлены в систему интервального повторения.\n"
        "Используй команду /review для повторения слов!\n"
        "Используй команду /test для проверки знаний!"
    )
    
    await message.answer(words_text)

def register_words_handlers(dp: Dispatcher):
    """Регистрация обработчиков команды words"""
    dp.message.register(cmd_words, F.text == "/words") 
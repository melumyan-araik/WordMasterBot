import random
from aiogram import Dispatcher, types, F
from database.models import get_user, get_words_by_level, update_test_results

async def cmd_test(message: types.Message):
    """Обработчик команды /test"""
    user_id = message.from_user.id
    
    # Получаем информацию о пользователе
    user = get_user(user_id)
    
    if not user:
        await message.answer(
            "Сначала нужно выбрать уровень! Напиши /start"
        )
        return
    
    # Получаем слова для тестирования
    words = get_words_by_level(user['level'], 20)
    
    if not words:
        await message.answer(
            f"К сожалению, для уровня {user['level']} пока нет слов в базе данных."
        )
        return
    
    # Выбираем случайное слово для тестирования
    test_word = random.choice(words)
    
    # Создаем варианты ответов
    correct_answer = test_word['translation']
    
    # Получаем другие переводы для создания неправильных вариантов
    wrong_answers = [word['translation'] for word in words 
                    if word['translation'] != correct_answer]
    
    # Выбираем 3 случайных неправильных ответа
    wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))
    
    all_answers = [correct_answer] + wrong_answers
    random.shuffle(all_answers)
    
    # Создаем клавиатуру с вариантами ответов
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=f"{chr(65+i)}) {answer}", callback_data=f"test_{test_word['word']}_{answer}")]
        for i, answer in enumerate(all_answers)
    ])
    
    # Экранируем специальные символы
    word = test_word['word'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    transcription = test_word['transcription'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    example = test_word['example'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    
    test_text = (
        f"🧪 Тест: {word}\n\n"
        f"Слово: {word} [{transcription}]\n"
        f"Пример: {example}\n\n"
        f"Как переводится это слово?"
    )
    
    await message.answer(test_text, reply_markup=keyboard)

async def process_test_answer(callback: types.CallbackQuery):
    """Обработка ответа на тест"""
    data = callback.data.split('_')
    word = data[1]
    selected_answer = data[2]
    
    # Получаем правильный ответ из базы данных
    from database.models import get_words_by_level
    user = get_user(callback.from_user.id)
    words = get_words_by_level(user['level'], 100)  # Получаем больше слов для поиска
    
    # Находим слово, которое тестировалось
    test_word = None
    for w in words:
        if w['word'] == word:
            test_word = w
            break
    
    if not test_word:
        await callback.answer("Ошибка: слово не найдено")
        return
    
    correct_answer = test_word['translation']
    is_correct = selected_answer == correct_answer
    
    # Обновляем результаты тестов
    update_test_results(callback.from_user.id, is_correct)
    
    # Экранируем специальные символы
    word = test_word['word'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    transcription = test_word['transcription'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    translation = correct_answer.replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    example = test_word['example'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    
    # Формируем ответ
    if is_correct:
        result_text = "✅ Верно! Отличная работа!"
    else:
        result_text = f"❌ Неправильно! Правильный ответ: {translation}"
    
    result_text += f"\n\nСлово: {word} [{transcription}]\n"
    result_text += f"Перевод: {translation}\n"
    result_text += f"Пример: {example}"
    
    await callback.message.edit_text(result_text)

def register_test_handlers(dp: Dispatcher):
    """Регистрация обработчиков команды test"""
    dp.message.register(cmd_test, F.text == "/test")
    dp.callback_query.register(process_test_answer, F.data.startswith("test_")) 
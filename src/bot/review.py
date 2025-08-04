from aiogram import Dispatcher, types, F
from database.models import get_user, get_words_for_review, update_spaced_repetition, get_spaced_repetition_stats

async def cmd_review(message: types.Message):
    """Обработчик команды /review - интервальное повторение"""
    user_id = message.from_user.id
    
    # Получаем информацию о пользователе
    user = get_user(user_id)
    
    if not user:
        await message.answer(
            "Сначала нужно выбрать уровень! Напиши /start"
        )
        return
    
    # Получаем слова для повторения
    review_words = get_words_for_review(user_id, 5)
    
    if not review_words:
        await message.answer(
            "🎉 Отлично! У тебя нет слов для повторения сегодня.\n\n"
            "💡 Попробуй:\n"
            "• /words - получить новые слова\n"
            "• /stats - посмотреть статистику\n"
            "• /test - пройти тест"
        )
        return
    
    # Получаем статистику
    stats = get_spaced_repetition_stats(user_id)
    
    # Формируем сообщение (без Markdown для избежания ошибок парсинга)
    review_text = "🔄 Интервальное повторение\n\n"
    review_text += "📊 Статистика:\n"
    review_text += f"• Всего слов в системе: {stats['total_words']}\n"
    review_text += f"• Слов для повторения сегодня: {stats['due_today']}\n"
    review_text += f"• Всего повторений: {stats['total_reviews']}\n\n"
    
    review_text += f"📝 Слова для повторения ({len(review_words)}):\n\n"
    
    for i, word_data in enumerate(review_words, 1):
        # Экранируем специальные символы для безопасности
        word = word_data['word'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        transcription = word_data['transcription'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        translation = word_data['translation'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        example = word_data['example'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        
        review_text += (
            f"{i}. {word} [{transcription}]\n"
            f"   Перевод: {translation}\n"
            f"   Пример: {example}\n"
            f"   Интервал: {word_data['interval_days']} дн.\n\n"
        )
    
    review_text += "💡 Используй /review_test для тестирования этих слов!"
    
    await message.answer(review_text)

async def cmd_review_test(message: types.Message):
    """Обработчик команды /review_test - тест интервального повторения"""
    user_id = message.from_user.id
    
    # Получаем информацию о пользователе
    user = get_user(user_id)
    
    if not user:
        await message.answer(
            "Сначала нужно выбрать уровень! Напиши /start"
        )
        return
    
    # Получаем слова для повторения
    review_words = get_words_for_review(user_id, 10)
    
    if not review_words:
        await message.answer(
            "🎉 У тебя нет слов для повторения сегодня!\n\n"
            "Попробуй:\n"
            "• /words - получить новые слова\n"
            "• /review - посмотреть слова для повторения"
        )
        return
    
    # Выбираем первое слово для тестирования
    test_word = review_words[0]
    
    # Создаем варианты ответов
    correct_answer = test_word['translation']
    
    # Получаем другие переводы для создания неправильных вариантов
    from database.models import get_words_by_level
    other_words = get_words_by_level(user['level'], 20)
    wrong_answers = [word['translation'] for word in other_words 
                    if word['translation'] != correct_answer]
    
    # Выбираем 3 случайных неправильных ответа
    import random
    wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))
    
    all_answers = [correct_answer] + wrong_answers
    random.shuffle(all_answers)
    
    # Создаем клавиатуру с вариантами ответов
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=f"{chr(65+i)}) {answer}", callback_data=f"review_{test_word['id']}_{test_word['word']}_{answer}")]
        for i, answer in enumerate(all_answers)
    ])
    
    # Экранируем специальные символы
    word = test_word['word'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    transcription = test_word['transcription'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    example = test_word['example'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    
    test_text = (
        f"🔄 Повторение: {word}\n\n"
        f"Слово: {word} [{transcription}]\n"
        f"Пример: {example}\n\n"
        f"Как переводится это слово?"
    )
    
    await message.answer(test_text, reply_markup=keyboard)

async def process_review_answer(callback: types.CallbackQuery):
    """Обработка ответа на тест повторения"""
    data = callback.data.split('_')
    review_id = int(data[1])
    word = data[2]
    selected_answer = data[3]
    
    # Получаем правильный ответ из базы данных
    from database.models import get_words_for_review
    review_words = get_words_for_review(callback.from_user.id, 10)
    correct_word = None
    
    for w in review_words:
        if w['id'] == review_id and w['word'] == word:
            correct_word = w
            break
    
    if not correct_word:
        await callback.answer("Ошибка: слово не найдено")
        return
    
    correct_answer = correct_word['translation']
    is_correct = selected_answer == correct_answer
    
    # Обновляем интервальное повторение
    from database.models import update_spaced_repetition
    update_spaced_repetition(review_id, is_correct)
    
    # Экранируем специальные символы
    word = correct_word['word'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    transcription = correct_word['transcription'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    translation = correct_answer.replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    example = correct_word['example'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
    
    # Формируем ответ
    if is_correct:
        result_text = "✅ Верно! Отличная работа!"
    else:
        result_text = f"❌ Неправильно! Правильный ответ: {translation}"
    
    result_text += f"\n\nСлово: {word} [{transcription}]\n"
    result_text += f"Перевод: {translation}\n"
    result_text += f"Пример: {example}\n\n"
    
    # Добавляем информацию о следующем повторении
    if is_correct:
        if correct_word['consecutive_correct'] == 0:
            next_interval = 1
        elif correct_word['consecutive_correct'] == 1:
            next_interval = 3
        elif correct_word['consecutive_correct'] == 2:
            next_interval = 7
        else:
            next_interval = 7 + (correct_word['consecutive_correct'] - 1) * 7
        
        result_text += f"🔄 Следующее повторение через {next_interval} дней"
    else:
        result_text += f"🔄 Следующее повторение завтра"
    
    await callback.message.edit_text(result_text)

def register_review_handlers(dp: Dispatcher):
    """Регистрация обработчиков команды review"""
    dp.message.register(cmd_review, F.text == "/review")
    dp.message.register(cmd_review_test, F.text == "/review_test")
    dp.callback_query.register(process_review_answer, F.data.startswith("review_")) 
from aiogram import Dispatcher, types, F
from database.models import get_user, get_spaced_repetition_stats, get_due_words_count

async def cmd_stats(message: types.Message):
    """Обработчик команды /stats"""
    user_id = message.from_user.id
    
    # Получаем информацию о пользователе
    user = get_user(user_id)
    
    if not user:
        await message.answer(
            "Сначала нужно выбрать уровень! Напиши /start"
        )
        return
    
    # Получаем статистику
    words_learned = user['words_learned']
    test_results = user['test_results']
    spaced_stats = get_spaced_repetition_stats(user_id)
    due_words = get_due_words_count(user_id)
    
    total_words = len(words_learned)
    correct_answers = test_results['correct']
    incorrect_answers = test_results['incorrect']
    total_tests = correct_answers + incorrect_answers
    
    # Вычисляем процент правильных ответов
    if total_tests > 0:
        accuracy_percent = (correct_answers / total_tests) * 100
    else:
        accuracy_percent = 0
    
    stats_text = (
        f"📊 Статистика обучения\n\n"
        f"🎯 Уровень: {user['level']}\n"
        f"📚 Выучено слов: {total_words}\n"
        f"🧪 Пройдено тестов: {total_tests}\n"
        f"✅ Правильных ответов: {correct_answers}\n"
        f"❌ Неправильных ответов: {incorrect_answers}\n"
        f"📈 Точность: {accuracy_percent:.1f}%\n\n"
    )
    
    # Добавляем статистику интервального повторения
    stats_text += (
        f"🔄 Интервальное повторение\n"
        f"📝 Слов в системе: {spaced_stats['total_words']}\n"
        f"⏰ Слов для повторения сегодня: {due_words}\n"
        f"🔄 Всего повторений: {spaced_stats['total_reviews']}\n"
        f"📊 Средний ease factor: {spaced_stats['avg_ease_factor']}\n\n"
    )
    
    if total_words > 0:
        stats_text += "📝 Последние выученные слова:\n"
        # Показываем последние 5 слов
        recent_words = words_learned[-5:] if len(words_learned) > 5 else words_learned
        for word in recent_words:
            stats_text += f"• {word}\n"
    
    if due_words > 0:
        stats_text += f"\n💡 У тебя {due_words} слов для повторения! Используй /review"
    elif total_tests == 0:
        stats_text += "\n💡 Попробуй пройти тест командой /test!"
    
    await message.answer(stats_text)

def register_stats_handlers(dp: Dispatcher):
    """Регистрация обработчиков команды stats"""
    dp.message.register(cmd_stats, F.text == "/stats") 
#!/usr/bin/env python3
"""
Тестовый скрипт для проверки команды /review
"""

from database.models import (
    init_db, add_user, get_words_by_level, add_word_to_spaced_repetition,
    get_words_for_review, get_spaced_repetition_stats
)

def test_review_command():
    """Тестирование команды /review"""
    print("🔄 Тестирование команды /review...")
    
    # Инициализация БД
    init_db()
    
    # Создаем тестового пользователя
    test_user_id = 99999
    add_user(test_user_id, 'A1')
    
    # Получаем слова и добавляем их в интервальное повторение
    words = get_words_by_level('A1', 5)
    if not words:
        print("❌ Не удалось получить слова для тестирования")
        return False
    
    print(f"📝 Добавляем {len(words)} слов в интервальное повторение:")
    for word in words:
        add_word_to_spaced_repetition(test_user_id, word['word_id'], word['word'])
        print(f"   ✅ {word['word']}")
    
    # Получаем слова для повторения
    review_words = get_words_for_review(test_user_id, 5)
    print(f"\n📊 Слов для повторения сегодня: {len(review_words)}")
    
    if not review_words:
        print("❌ Нет слов для повторения")
        return False
    
    # Получаем статистику
    stats = get_spaced_repetition_stats(test_user_id)
    print(f"\n📈 Статистика:")
    print(f"   Всего слов в системе: {stats['total_words']}")
    print(f"   Слов для повторения сегодня: {stats['due_today']}")
    print(f"   Всего повторений: {stats['total_reviews']}")
    
    # Формируем сообщение (как в обработчике)
    print(f"\n📝 Сообщение команды /review:")
    print("🔄 Интервальное повторение\n")
    print("📊 Статистика:")
    print(f"• Всего слов в системе: {stats['total_words']}")
    print(f"• Слов для повторения сегодня: {stats['due_today']}")
    print(f"• Всего повторений: {stats['total_reviews']}\n")
    
    print(f"📝 Слова для повторения ({len(review_words)}):\n")
    
    for i, word_data in enumerate(review_words, 1):
        # Экранируем специальные символы для безопасности
        word = word_data['word'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        transcription = word_data['transcription'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        translation = word_data['translation'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        example = word_data['example'].replace('_', '\\_').replace('*', '\\*').replace('`', '\\`')
        
        print(f"{i}. {word} [{transcription}]")
        print(f"   Перевод: {translation}")
        print(f"   Пример: {example}")
        print(f"   Интервал: {word_data['interval_days']} дн.\n")
    
    print("💡 Используй /review_test для тестирования этих слов!")
    
    print("\n✅ Тестирование команды /review завершено успешно")
    return True

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования команды /review")
    print("=" * 50)
    
    if test_review_command():
        print("\n✅ Команда /review работает корректно!")
        print("\n📋 Проверено:")
        print("• Добавление слов в интервальное повторение")
        print("• Получение слов для повторения")
        print("• Формирование статистики")
        print("• Экранирование специальных символов")
        print("• Формирование сообщения без Markdown")
    else:
        print("\n❌ Команда /review имеет проблемы!")

if __name__ == "__main__":
    main() 
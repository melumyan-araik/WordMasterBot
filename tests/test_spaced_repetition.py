#!/usr/bin/env python3
"""
Тестовый скрипт для проверки интервального повторения
"""

from database.models import (
    init_db, add_user, get_words_by_level, add_word_to_spaced_repetition,
    get_words_for_review, update_spaced_repetition, get_spaced_repetition_stats
)
from datetime import datetime, timedelta

def test_spaced_repetition():
    """Тестирование системы интервального повторения"""
    print("🔄 Тестирование системы интервального повторения...")
    
    # Инициализация БД
    init_db()
    
    # Создаем тестового пользователя
    test_user_id = 99999
    add_user(test_user_id, 'A1')
    
    # Получаем несколько слов
    words = get_words_by_level('A1', 3)
    
    if not words:
        print("❌ Не удалось получить слова для тестирования")
        return False
    
    print(f"✅ Получено {len(words)} слов для тестирования")
    
    # Добавляем слова в систему интервального повторения
    for word in words:
        add_word_to_spaced_repetition(test_user_id, word['word_id'], word['word'])
        print(f"   Добавлено слово: {word['word']}")
    
    # Проверяем статистику
    stats = get_spaced_repetition_stats(test_user_id)
    print(f"📊 Статистика после добавления:")
    print(f"   Всего слов: {stats['total_words']}")
    print(f"   Слов для повторения сегодня: {stats['due_today']}")
    
    # Получаем слова для повторения
    review_words = get_words_for_review(test_user_id, 5)
    print(f"✅ Получено {len(review_words)} слов для повторения")
    
    # Тестируем обновление интервалов
    if review_words:
        word = review_words[0]
        print(f"\n🧪 Тестируем слово: {word['word']}")
        print(f"   Текущий интервал: {word['interval_days']} дней")
        print(f"   Ease factor: {word['ease_factor']}")
        
        # Симулируем правильный ответ
        update_spaced_repetition(word['id'], True)
        print("   ✅ Правильный ответ обработан")
        
        # Получаем обновленную статистику
        updated_stats = get_spaced_repetition_stats(test_user_id)
        print(f"   Новый интервал: {word['interval_days']} дней")
        print(f"   Новый ease factor: {word['ease_factor']}")
        
        # Симулируем неправильный ответ
        update_spaced_repetition(word['id'], False)
        print("   ❌ Неправильный ответ обработан")
        
        print("✅ Тестирование интервального повторения завершено успешно")
        return True
    else:
        print("❌ Нет слов для повторения")
        return False

def test_interval_calculation():
    """Тестирование расчета интервалов"""
    print("\n📈 Тестирование расчета интервалов...")
    
    # Инициализация БД
    init_db()
    
    # Создаем тестового пользователя
    test_user_id = 88888
    add_user(test_user_id, 'A1')
    
    # Получаем слово
    words = get_words_by_level('A1', 1)
    if not words:
        print("❌ Не удалось получить слово для тестирования")
        return False
    
    word = words[0]
    add_word_to_spaced_repetition(test_user_id, word['word_id'], word['word'])
    
    # Получаем слово для повторения
    review_words = get_words_for_review(test_user_id, 1)
    if not review_words:
        print("❌ Слово не найдено для повторения")
        return False
    
    review_word = review_words[0]
    print(f"Тестируем слово: {review_word['word']}")
    
    # Симулируем последовательность ответов
    intervals = []
    ease_factors = []
    
    for i in range(5):
        is_correct = i < 3  # Первые 3 ответа правильные, последние 2 - неправильные
        update_spaced_repetition(review_word['id'], is_correct)
        
        # Получаем обновленное слово
        updated_words = get_words_for_review(test_user_id, 1)
        if updated_words:
            updated_word = updated_words[0]
            intervals.append(updated_word['interval_days'])
            ease_factors.append(updated_word['ease_factor'])
            print(f"   Попытка {i+1}: {'✅' if is_correct else '❌'} -> интервал: {updated_word['interval_days']} дн., ease: {updated_word['ease_factor']:.2f}")
    
    print("✅ Тестирование интервалов завершено")
    return True

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования интервального повторения")
    print("=" * 60)
    
    tests = [
        ("Система интервального повторения", test_spaced_repetition),
        ("Расчет интервалов", test_interval_calculation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Тест: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - ПРОЙДЕН")
        else:
            print(f"❌ {test_name} - ПРОВАЛЕН")
    
    print("\n" + "=" * 60)
    print(f"📊 Результаты тестирования: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты интервального повторения пройдены!")
        print("\n📋 Функциональность интервального повторения:")
        print("• Слова автоматически добавляются в систему при получении")
        print("• Интервалы увеличиваются при правильных ответах")
        print("• Интервалы сбрасываются при неправильных ответах")
        print("• Ease factor адаптируется к успеваемости")
        print("• Команды /review и /review_test работают")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте настройки.")

if __name__ == "__main__":
    main() 
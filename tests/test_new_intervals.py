#!/usr/bin/env python3
"""
Тестовый скрипт для проверки нового алгоритма интервалов
"""

from database.models import (
    init_db, add_user, get_words_by_level, add_word_to_spaced_repetition,
    get_words_for_review, update_spaced_repetition
)
from datetime import datetime, timedelta

def test_new_interval_algorithm():
    """Тестирование нового алгоритма интервалов"""
    print("🔄 Тестирование нового алгоритма интервалов...")
    
    # Инициализация БД
    init_db()
    
    # Создаем тестового пользователя
    test_user_id = 77777
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
    
    # Симулируем последовательность правильных ответов
    print("\n📈 Симуляция правильных ответов:")
    
    for i in range(5):
        update_spaced_repetition(review_word['id'], True)
        
        # Получаем обновленное слово
        updated_words = get_words_for_review(test_user_id, 1)
        if updated_words:
            updated_word = updated_words[0]
            consecutive_correct = updated_word['consecutive_correct']
            
            # Вычисляем ожидаемый интервал
            if consecutive_correct == 1:
                expected_interval = 1
            elif consecutive_correct == 2:
                expected_interval = 3
            elif consecutive_correct == 3:
                expected_interval = 7
            else:
                expected_interval = 7 + (consecutive_correct - 3) * 7
            
            print(f"   Попытка {i+1}: ✅ -> интервал: {updated_word['interval_days']} дн. (ожидается: {expected_interval})")
            
            # Проверяем правильность
            if updated_word['interval_days'] == expected_interval:
                print(f"   ✅ Интервал корректен!")
            else:
                print(f"   ❌ Ошибка в интервале!")
                return False
    
    # Симулируем неправильный ответ
    print("\n📉 Симуляция неправильного ответа:")
    update_spaced_repetition(review_word['id'], False)
    
    updated_words = get_words_for_review(test_user_id, 1)
    if updated_words:
        updated_word = updated_words[0]
        print(f"   ❌ Неправильный ответ -> интервал: {updated_word['interval_days']} дн.")
        
        if updated_word['interval_days'] == 1:
            print("   ✅ Интервал сброшен корректно!")
        else:
            print("   ❌ Ошибка в сбросе интервала!")
            return False
    
    print("✅ Тестирование нового алгоритма интервалов завершено успешно")
    return True

def test_interval_sequence():
    """Тестирование последовательности интервалов"""
    print("\n📊 Тестирование последовательности интервалов...")
    
    # Инициализация БД
    init_db()
    
    # Создаем тестового пользователя
    test_user_id = 66666
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
    
    # Ожидаемая последовательность интервалов
    expected_intervals = [1, 3, 7, 14, 21, 28, 35]
    
    print("\n📋 Ожидаемая последовательность интервалов:")
    for i, interval in enumerate(expected_intervals):
        print(f"   {i+1}-й правильный ответ: {interval} дней")
    
    print("\n🧪 Симуляция последовательности:")
    
    for i in range(len(expected_intervals)):
        update_spaced_repetition(review_word['id'], True)
        
        # Получаем обновленное слово
        updated_words = get_words_for_review(test_user_id, 1)
        if updated_words:
            updated_word = updated_words[0]
            actual_interval = updated_word['interval_days']
            expected_interval = expected_intervals[i]
            
            print(f"   {i+1}-й ответ: {actual_interval} дн. (ожидается: {expected_interval})")
            
            if actual_interval == expected_interval:
                print(f"   ✅ Корректно!")
            else:
                print(f"   ❌ Ошибка!")
                return False
    
    print("✅ Последовательность интервалов корректна!")
    return True

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования нового алгоритма интервалов")
    print("=" * 60)
    
    tests = [
        ("Новый алгоритм интервалов", test_new_interval_algorithm),
        ("Последовательность интервалов", test_interval_sequence),
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
        print("🎉 Все тесты нового алгоритма интервалов пройдены!")
        print("\n📋 Новый алгоритм интервального повторения:")
        print("• 1-й правильный ответ: 1 день")
        print("• 2-й правильный ответ: 3 дня")
        print("• 3-й правильный ответ: 7 дней (неделя)")
        print("• 4-й правильный ответ: 14 дней (2 недели)")
        print("• 5-й правильный ответ: 21 день (3 недели)")
        print("• И так далее...")
        print("• Неправильный ответ: сброс на 1 день")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте настройки.")

if __name__ == "__main__":
    main() 
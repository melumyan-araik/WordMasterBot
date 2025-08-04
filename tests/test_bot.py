#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функциональности бота
"""

from database.models import init_db, get_words_by_level, get_user, add_user
import sqlite3
from config import DATABASE_PATH

def test_database():
    """Тестирование базы данных"""
    print("🧪 Тестирование базы данных...")
    
    # Инициализация БД
    init_db()
    
    # Проверка подключения
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Проверка таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ Найдены таблицы: {[table[0] for table in tables]}")
        
        # Проверка количества слов
        cursor.execute("SELECT level, COUNT(*) FROM words GROUP BY level;")
        word_counts = cursor.fetchall()
        print("📊 Количество слов по уровням:")
        for level, count in word_counts:
            print(f"   - {level}: {count} слов")
        
        # Тест получения слов
        words_a1 = get_words_by_level('A1', 5)
        print(f"✅ Получено {len(words_a1)} слов уровня A1")
        
        words_b1 = get_words_by_level('B1', 5)
        print(f"✅ Получено {len(words_b1)} слов уровня B1")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании БД: {e}")
        return False

def test_user_management():
    """Тестирование управления пользователями"""
    print("\n👤 Тестирование управления пользователями...")
    
    try:
        # Добавление тестового пользователя
        test_user_id = 12345
        add_user(test_user_id, 'B1')
        
        # Получение пользователя
        user = get_user(test_user_id)
        if user:
            print(f"✅ Пользователь создан: ID={user['user_id']}, Уровень={user['level']}")
            return True
        else:
            print("❌ Не удалось получить пользователя")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании пользователей: {e}")
        return False

def test_word_format():
    """Тестирование формата слов"""
    print("\n📝 Тестирование формата слов...")
    
    try:
        words = get_words_by_level('A1', 1)
        if words:
            word = words[0]
            required_fields = ['word', 'transcription', 'translation', 'example', 'level']
            
            for field in required_fields:
                if field not in word:
                    print(f"❌ Отсутствует поле: {field}")
                    return False
            
            print(f"✅ Формат слова корректный:")
            print(f"   Слово: {word['word']}")
            print(f"   Транскрипция: {word['transcription']}")
            print(f"   Перевод: {word['translation']}")
            print(f"   Пример: {word['example']}")
            print(f"   Уровень: {word['level']}")
            return True
        else:
            print("❌ Не удалось получить слова")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании формата слов: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования MVP Telegram-бота")
    print("=" * 50)
    
    tests = [
        ("База данных", test_database),
        ("Управление пользователями", test_user_management),
        ("Формат слов", test_word_format),
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
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты тестирования: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Бот готов к запуску.")
        print("\n📋 Следующие шаги:")
        print("1. Создайте бота через @BotFather")
        print("2. Добавьте токен в config.py или .env файл")
        print("3. Запустите: python main.py")
    else:
        print("⚠️  Некоторые тесты не пройдены. Проверьте настройки.")

if __name__ == "__main__":
    main() 
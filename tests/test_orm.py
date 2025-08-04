#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы ORM
"""
import sys
import os

# Добавляем src в путь для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.models import Session, User, Word, SpacedRepetition, get_words_by_level, add_user

def test_orm():
    """Тестирование работы ORM"""
    print("Тестирование работы SQLAlchemy ORM...")
    
    # Создаем сессию
    session = Session()
    
    try:
        # Тест 1: Получение слов по уровню
        print("\n1. Тест получения слов по уровню A1:")
        words = get_words_by_level('A1', limit=5)
        for word in words:
            print(f"  - {word['word']} ({word['translation']})")
        
        # Тест 2: Добавление пользователя
        print("\n2. Тест добавления пользователя:")
        add_user(12345, 'A2')
        print("  Пользователь добавлен")
        
        # Тест 3: Проверка количества слов в базе
        print("\n3. Проверка количества слов в базе:")
        total_words = session.query(Word).count()
        print(f"  Всего слов в базе: {total_words}")
        
        # Тест 4: Проверка слов по уровням
        print("\n4. Количество слов по уровням:")
        for level in ['A1', 'A2', 'B1', 'B2']:
            count = session.query(Word).filter(Word.level == level).count()
            print(f"  {level}: {count} слов")
        
        # Тест 5: Проверка структуры таблиц
        print("\n5. Проверка структуры таблиц:")
        users_count = session.query(User).count()
        print(f"  Пользователей: {users_count}")
        
        spaced_rep_count = session.query(SpacedRepetition).count()
        print(f"  Записей интервального повторения: {spaced_rep_count}")
        
        print("\n✅ Все тесты прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    test_orm() 
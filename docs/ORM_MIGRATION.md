# Миграция на SQLAlchemy ORM

## Описание изменений

Проект был успешно переписан для использования SQLAlchemy ORM вместо прямых SQL запросов.

## Основные изменения

### 1. Модели данных (src/database/models.py)

**Было:**
- Прямые SQL запросы с использованием `sqlite3`
- Ручное управление соединениями
- Отсутствие типизации

**Стало:**
- SQLAlchemy ORM модели с декларативным синтаксисом
- Автоматическое управление сессиями
- Строгая типизация полей
- Связи между таблицами через `relationship`

### 2. Структура моделей

```python
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    level = Column(String(10), nullable=False, default='A1')
    # ... другие поля

class Word(Base):
    __tablename__ = 'words'
    word_id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(100), nullable=False)
    # ... другие поля

class SpacedRepetition(Base):
    __tablename__ = 'spaced_repetition'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    word_id = Column(Integer, ForeignKey('words.word_id'), nullable=False)
    # ... другие поля
```

### 3. Преимущества ORM

1. **Безопасность**: Защита от SQL-инъекций
2. **Типизация**: Строгая типизация полей
3. **Удобство**: Декларативный синтаксис
4. **Производительность**: Автоматическая оптимизация запросов
5. **Поддержка**: Лучшая поддержка различных СУБД

### 4. Зависимости

Добавлена зависимость в `requirements.txt`:
```
SQLAlchemy>=2.0.0
```

### 5. Функциональность

Все существующие функции сохранены:
- ✅ Добавление пользователей
- ✅ Получение слов по уровню
- ✅ Интервальное повторение
- ✅ Статистика
- ✅ Заполнение базы данных

### 6. Тестирование

Создан тестовый скрипт `test_orm.py` для проверки:
- Получения слов по уровню
- Добавления пользователей
- Подсчета записей
- Структуры таблиц

## Запуск

1. Установка зависимостей:
```bash
pip install -r requirements.txt
```

2. Заполнение базы данных:
```bash
python populate_db.py
```

3. Тестирование ORM:
```bash
python test_orm.py
```

## Результат

- ✅ База данных успешно создана
- ✅ 263 слова добавлены (A1: 69, A2: 62, B1: 66, B2: 66)
- ✅ Все функции работают корректно
- ✅ ORM полностью интегрирован

## Структура базы данных

```
users
├── user_id (PK)
├── level
├── words_learned (JSON)
├── test_results (JSON)
└── created_at

words
├── word_id (PK)
├── word
├── transcription
├── translation
├── example
└── level

spaced_repetition
├── id (PK)
├── user_id (FK -> users)
├── word_id (FK -> words)
├── word
├── interval_days
├── next_review_date
├── ease_factor
├── consecutive_correct
├── consecutive_incorrect
├── total_reviews
├── last_review_date
└── created_at
``` 
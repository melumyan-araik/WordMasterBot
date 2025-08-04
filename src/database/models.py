from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional
from .config import DATABASE_PATH

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем движок базы данных
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=False)
Session = sessionmaker(bind=engine)

class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    level = Column(String(10), nullable=False, default='A1')
    words_learned = Column(Text, default='[]')
    test_results = Column(Text, default='{"correct": 0, "incorrect": 0}')
    created_at = Column(DateTime, default=datetime.now)
    
    # Связь с интервальным повторением
    spaced_repetitions = relationship("SpacedRepetition", back_populates="user")

class Word(Base):
    """Модель слова"""
    __tablename__ = 'words'
    
    word_id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(100), nullable=False)
    transcription = Column(String(100), nullable=False)
    translation = Column(String(200), nullable=False)
    example = Column(Text, nullable=False)
    level = Column(String(10), nullable=False)
    
    # Связь с интервальным повторением
    spaced_repetitions = relationship("SpacedRepetition", back_populates="word_obj")

class SpacedRepetition(Base):
    """Модель интервального повторения"""
    __tablename__ = 'spaced_repetition'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    word_id = Column(Integer, ForeignKey('words.word_id'), nullable=False)
    word = Column(String(100), nullable=False)  # Дублируем слово для удобства
    interval_days = Column(Integer, default=1)
    next_review_date = Column(Date, nullable=False)
    ease_factor = Column(Float, default=2.5)
    consecutive_correct = Column(Integer, default=0)
    consecutive_incorrect = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    last_review_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)
    
    # Связи
    user = relationship("User", back_populates="spaced_repetitions")
    word_obj = relationship("Word", back_populates="spaced_repetitions")
    
    # Уникальное ограничение
    __table_args__ = (UniqueConstraint('user_id', 'word_id'),)

def init_db():
    """Инициализация базы данных"""
    Base.metadata.create_all(engine)

def add_user(user_id: int, level: str = 'A1'):
    """Добавление нового пользователя"""
    session = Session()
    try:
        user = User(user_id=user_id, level=level)
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_user(user_id: int) -> Optional[Dict]:
    """Получение информации о пользователе"""
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return {
                'user_id': user.user_id,
                'level': user.level,
                'words_learned': json.loads(user.words_learned),
                'test_results': json.loads(user.test_results),
                'created_at': user.created_at
            }
        return None
    finally:
        session.close()

def update_user_level(user_id: int, level: str):
    """Обновление уровня пользователя"""
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            user.level = level
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def add_learned_word(user_id: int, word: str):
    """Добавление выученного слова"""
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            words_learned = json.loads(user.words_learned)
            if word not in words_learned:
                words_learned.append(word)
                user.words_learned = json.dumps(words_learned)
                session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_test_results(user_id: int, is_correct: bool):
    """Обновление результатов тестов"""
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            test_results = json.loads(user.test_results)
            if is_correct:
                test_results['correct'] += 1
            else:
                test_results['incorrect'] += 1
            user.test_results = json.dumps(test_results)
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_words_by_level(level: str, limit: int = 5) -> List[Dict]:
    """Получение слов по уровню"""
    session = Session()
    try:
        words = session.query(Word).filter(Word.level == level).order_by(Word.word_id).limit(limit).all()
        return [
            {
                'word_id': word.word_id,
                'word': word.word,
                'transcription': word.transcription,
                'translation': word.translation,
                'example': word.example,
                'level': word.level
            }
            for word in words
        ]
    finally:
        session.close()

def get_word_by_id(word_id: int) -> Optional[Dict]:
    """Получение слова по ID"""
    session = Session()
    try:
        word = session.query(Word).filter(Word.word_id == word_id).first()
        if word:
            return {
                'word_id': word.word_id,
                'word': word.word,
                'transcription': word.transcription,
                'translation': word.translation,
                'example': word.example,
                'level': word.level
            }
        return None
    finally:
        session.close()

def add_word(word: str, transcription: str, translation: str, example: str, level: str):
    """Добавление нового слова в базу"""
    session = Session()
    try:
        new_word = Word(
            word=word,
            transcription=transcription,
            translation=translation,
            example=example,
            level=level
        )
        session.add(new_word)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Функции для интервального повторения

def add_word_to_spaced_repetition(user_id: int, word_id: int, word: str):
    """Добавление слова в систему интервального повторения"""
    session = Session()
    try:
        # Устанавливаем следующую дату повторения на сегодня (для немедленного повторения)
        next_review = datetime.now().date()
        
        spaced_rep = SpacedRepetition(
            user_id=user_id,
            word_id=word_id,
            word=word,
            next_review_date=next_review
        )
        session.add(spaced_rep)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_words_for_review(user_id: int, limit: int = 10) -> List[Dict]:
    """Получение слов для повторения на сегодня"""
    session = Session()
    try:
        today = datetime.now().date()
        
        # Используем join для получения полной информации о словах
        results = session.query(
            SpacedRepetition, Word
        ).join(
            Word, SpacedRepetition.word_id == Word.word_id
        ).filter(
            SpacedRepetition.user_id == user_id,
            SpacedRepetition.next_review_date <= today
        ).order_by(
            SpacedRepetition.next_review_date.asc()
        ).limit(limit).all()
        
        return [
            {
                'id': sr.id,
                'word_id': sr.word_id,
                'word': sr.word,
                'interval_days': sr.interval_days,
                'ease_factor': sr.ease_factor,
                'consecutive_correct': sr.consecutive_correct,
                'consecutive_incorrect': sr.consecutive_incorrect,
                'total_reviews': sr.total_reviews,
                'transcription': word.transcription,
                'translation': word.translation,
                'example': word.example,
                'level': word.level
            }
            for sr, word in results
        ]
    finally:
        session.close()

def update_spaced_repetition(review_id: int, is_correct: bool):
    """Обновление интервального повторения после ответа пользователя"""
    session = Session()
    try:
        spaced_rep = session.query(SpacedRepetition).filter(SpacedRepetition.id == review_id).first()
        
        if not spaced_rep:
            return
        
        # Обновляем счетчики
        if is_correct:
            spaced_rep.consecutive_correct += 1
            spaced_rep.consecutive_incorrect = 0
        else:
            spaced_rep.consecutive_incorrect += 1
            spaced_rep.consecutive_correct = 0
        
        spaced_rep.total_reviews += 1
        spaced_rep.last_review_date = datetime.now().date()
        
        # Вычисляем новый интервал и ease factor
        if is_correct:
            # Увеличиваем интервал по новому алгоритму
            if spaced_rep.consecutive_correct == 0:  # Первый правильный ответ
                spaced_rep.interval_days = 1
            elif spaced_rep.consecutive_correct == 1:  # Второй правильный ответ
                spaced_rep.interval_days = 3
            elif spaced_rep.consecutive_correct == 2:  # Третий правильный ответ
                spaced_rep.interval_days = 7
            else:
                # После третьего правильного ответа интервал увеличивается на неделю
                spaced_rep.interval_days = 7 + (spaced_rep.consecutive_correct - 2) * 7
            
            # Увеличиваем ease factor (но не более 2.5)
            spaced_rep.ease_factor = min(2.5, spaced_rep.ease_factor + 0.1)
        else:
            # Сбрасываем интервал
            spaced_rep.interval_days = 1
            spaced_rep.consecutive_correct = 0
            
            # Уменьшаем ease factor (но не менее 1.3)
            spaced_rep.ease_factor = max(1.3, spaced_rep.ease_factor - 0.2)
        
        # Вычисляем следующую дату повторения
        spaced_rep.next_review_date = datetime.now().date() + timedelta(days=spaced_rep.interval_days)
        
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_spaced_repetition_stats(user_id: int) -> Dict:
    """Получение статистики интервального повторения"""
    session = Session()
    try:
        today = datetime.now().date()
        
        # Общая статистика
        total_words = session.query(SpacedRepetition).filter(SpacedRepetition.user_id == user_id).count()
        due_today = session.query(SpacedRepetition).filter(
            SpacedRepetition.user_id == user_id,
            SpacedRepetition.next_review_date <= today
        ).count()
        
        # Средний ease factor
        avg_ease_result = session.query(SpacedRepetition.ease_factor).filter(
            SpacedRepetition.user_id == user_id
        ).all()
        avg_ease_factor = sum(row[0] for row in avg_ease_result) / len(avg_ease_result) if avg_ease_result else 0
        
        # Общее количество повторений
        total_reviews_result = session.query(SpacedRepetition.total_reviews).filter(
            SpacedRepetition.user_id == user_id
        ).all()
        total_reviews = sum(row[0] for row in total_reviews_result) if total_reviews_result else 0
        
        return {
            'total_words': total_words,
            'due_today': due_today,
            'avg_ease_factor': round(avg_ease_factor, 2),
            'total_reviews': total_reviews
        }
    finally:
        session.close()

def get_due_words_count(user_id: int) -> int:
    """Получение количества слов для повторения сегодня"""
    session = Session()
    try:
        today = datetime.now().date()
        return session.query(SpacedRepetition).filter(
            SpacedRepetition.user_id == user_id,
            SpacedRepetition.next_review_date <= today
        ).count()
    finally:
        session.close() 
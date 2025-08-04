#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных словами
"""
import sys
import os

# Добавляем src в путь для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scripts.populate_database import populate_words

if __name__ == "__main__":
    print("Заполнение базы данных словами...")
    populate_words()
    print("База данных успешно заполнена!") 
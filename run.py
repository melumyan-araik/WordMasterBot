#!/usr/bin/env python3
"""
Точка входа для запуска бота
"""
import sys
import os

# Добавляем src в путь для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from bot.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main()) 
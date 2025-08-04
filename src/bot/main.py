import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from .config import BOT_TOKEN
from database.models import init_db
from . import register_all_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    """Основная функция запуска бота"""
    logging.info("Бот запускается...")
    
    # Инициализация бота без Markdown
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Регистрация всех обработчиков
    register_all_handlers(dp)
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 
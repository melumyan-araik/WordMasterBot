from aiogram import Dispatcher
from .start import register_start_handlers
from .words import register_words_handlers
from .test import register_test_handlers
from .stats import register_stats_handlers
from .help import register_help_handlers
from .review import register_review_handlers

def register_all_handlers(dp: Dispatcher):
    """Регистрация всех обработчиков"""
    register_start_handlers(dp)
    register_words_handlers(dp)
    register_test_handlers(dp)
    register_stats_handlers(dp)
    register_help_handlers(dp)
    register_review_handlers(dp) 
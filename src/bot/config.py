import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Токен бота (замените на свой токен от BotFather)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token_here')

# Настройки базы данных
DATABASE_PATH = 'words_bot.db'

# Настройки бота
WORDS_PER_DAY = 5
TEST_DELAY_HOURS = 1  # Задержка перед показом теста в часах 
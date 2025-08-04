from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.models import add_user, get_user

class UserLevel(StatesGroup):
    waiting_for_level = State()

async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    
    # Проверяем, существует ли пользователь
    user = get_user(user_id)
    
    if user:
        # Пользователь уже существует
        await message.answer(
            f"С возвращением! Твой текущий уровень: {user['level']}\n\n"
            "Используй команды:\n"
            "/words - получить 5 слов\n"
            "/review - интервальное повторение\n"
            "/test - пройти тест\n"
            "/stats - статистика\n"
            "/help - помощь"
        )
    else:
        # Новый пользователь
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="A1 (Начинающий)", callback_data="level_A1"),
                types.InlineKeyboardButton(text="A2 (Элементарный)", callback_data="level_A2")
            ],
            [
                types.InlineKeyboardButton(text="B1 (Средний)", callback_data="level_B1"),
                types.InlineKeyboardButton(text="B2 (Выше среднего)", callback_data="level_B2")
            ]
        ])
        
        await message.answer(
            "Привет! 👋 Я помогу тебе выучить английские слова.\n\n"
            "Выбери свой уровень английского языка:",
            reply_markup=keyboard
        )
        await state.set_state(UserLevel.waiting_for_level)

async def process_level_selection(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора уровня"""
    level = callback.data.split('_')[1]
    user_id = callback.from_user.id
    
    # Сохраняем пользователя в базе данных
    add_user(user_id, level)
    
    await state.clear()
    
    await callback.message.edit_text(
        f"Отлично! Твой уровень: {level}\n\n"
        "Теперь ты будешь получать 5 слов в день для изучения.\n\n"
        "Команды:\n"
        "📚 /words - получить 5 слов\n"
        "🔄 /review - интервальное повторение\n"
        "🧪 /test - пройти тест\n"
        "📊 /stats - статистика\n"
        "❓ /help - помощь\n\n"
        "Напиши /words, чтобы начать изучение!"
    )

def register_start_handlers(dp: Dispatcher):
    """Регистрация обработчиков команды start"""
    dp.message.register(cmd_start, F.text == "/start")
    dp.callback_query.register(process_level_selection, F.data.startswith("level_")) 
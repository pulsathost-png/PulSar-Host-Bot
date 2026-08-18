from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Статистика"),
            KeyboardButton(text="👥 Пользователи")
        ],
        [
            KeyboardButton(text="🖥 Серверы"),
            KeyboardButton(text="💰 Выдать баланс")
        ],
        [
            KeyboardButton(text="🎫 Создать промокод")
        ],
        [
            KeyboardButton(text="⬅️ Выйти из админки")
        ]
    ],
    resize_keyboard=True
)

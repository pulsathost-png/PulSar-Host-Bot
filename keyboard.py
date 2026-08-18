from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Профиль"),
            KeyboardButton(text="💰 Баланс")
        ],
        [
            KeyboardButton(text="🖥 Мои серверы"),
            KeyboardButton(text="🛒 Купить сервер")
        ],
        [
            KeyboardButton(text="🎫 Промокод"),
            KeyboardButton(text="🆘 Поддержка")
        ]
    ],
    resize_keyboard=True
)

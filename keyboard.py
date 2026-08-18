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
            KeyboardButton(text="▶️ Запустить сервер"),
            KeyboardButton(text="⏹ Остановить сервер")
        ],
        [
            KeyboardButton(text="📟 Консоль"),
            KeyboardButton(text="🎫 Промокод")
        ],
        [
            KeyboardButton(text="🆘 Поддержка")
        ]
    ],
    resize_keyboard=True
)


plans_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🟢 START - 50₽")
        ],
        [
            KeyboardButton(text="🔵 PRO - 100₽")
        ],
        [
            KeyboardButton(text="🟣 ULTRA - 500₽")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True
)

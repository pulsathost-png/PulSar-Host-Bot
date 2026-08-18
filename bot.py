import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from config import BOT_TOKEN
from database import create_tables
from admin import router as admin_router
from services.promo import get_promo, use_promo


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

# Подключаем админ-панель
dp.include_router(admin_router)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🚀 Добро пожаловать в PulSar-Host!\n\n"
        "🎮 Игровой хостинг через Telegram\n"
        "Версия: 1.0\n\n"
        "Команды:\n"
        "/start — запуск\n"
        "/promo КОД — активировать промокод\n"
        "/admin — админ-панель"
    )


@dp.message(Command("promo"))
async def promo_activate(message: Message):
    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "🎫 Использование:\n"
            "/promo КОД"
        )
        return

    code = args[1]

    promo = get_promo(code)

    if not promo:
        await message.answer(
            "❌ Промокод не найден."
        )
        return

    if promo[2] <= 0:
        await message.answer(
            "❌ Промокод закончился."
        )
        return

    use_promo(code)

    await message.answer(
        f"✅ Промокод активирован!\n\n"
        f"💰 Бонус: {promo[1]}₽"
    )


@dp.message()
async def message_handler(message: Message):
    await message.answer(
        "Используй /start для открытия меню."
    )


async def main():
    create_tables()

    print("🚀 PulSar-Host Bot запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

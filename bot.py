import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from config import BOT_TOKEN
from database import (
    create_tables,
    add_user,
    get_balance,
    add_balance
)

from admin import router as admin_router
from services.promo import get_promo, use_promo


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()

dp.include_router(admin_router)


@dp.message(Command("start"))
async def start(message: Message):
    add_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "🚀 Добро пожаловать в PulSar-Host!\n\n"
        "🎮 Игровой хостинг через Telegram\n\n"
        "Команды:\n"
        "/balance — мой баланс\n"
        "/promo КОД — активировать промокод\n"
        "/admin — админ-панель"
    )


@dp.message(Command("balance"))
async def balance(message: Message):
    money = get_balance(message.from_user.id)

    await message.answer(
        f"💰 Ваш баланс: {money}₽"
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

    add_balance(
        message.from_user.id,
        promo[1]
    )

    use_promo(code)

    await message.answer(
        f"✅ Промокод активирован!\n\n"
        f"💰 На баланс добавлено: {promo[1]}₽"
    )


@dp.message()
async def message_handler(message: Message):
    await message.answer(
        "Используй /start"
    )


async def main():
    create_tables()

    print("🚀 PulSar-Host Bot 1.0 запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

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

from services.promo import (
    get_promo,
    use_promo
)

from services.servers import (
    create_server,
    get_servers,
    start_server,
    stop_server
)

from services.console import send_command

from keyboard import main_menu


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
        "🎮 Игровой хостинг через Telegram\n"
        "Версия: 1.0\n\n"
        "Выберите действие:",
        reply_markup=main_menu
    )


@dp.message(Command("balance"))
async def balance(message: Message):

    money = get_balance(message.from_user.id)

    await message.answer(
        f"💰 Баланс: {money}₽"
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
            "❌ Промокод не найден"
        )
        return

    if promo[2] <= 0:
        await message.answer(
            "❌ Промокод закончился"
        )
        return

    add_balance(
        message.from_user.id,
        promo[1]
    )

    use_promo(code)

    await message.answer(
        f"✅ Промокод активирован!\n"
        f"💰 +{promo[1]}₽"
    )


@dp.message(lambda m: m.text == "💰 Баланс")
async def balance_button(message: Message):

    money = get_balance(message.from_user.id)

    await message.answer(
        f"💰 Ваш баланс: {money}₽"
    )


@dp.message(lambda m: m.text == "👤 Профиль")
async def profile(message: Message):

    await message.answer(
        f"👤 Профиль\n\n"
        f"ID: {message.from_user.id}"
    )


@dp.message(lambda m: m.text == "🛒 Купить сервер")
async def buy_server(message: Message):

    create_server(
        message.from_user.id,
        "PulSar Server"
    )

    await message.answer(
        "✅ Сервер создан!\n"
        "🖥 PulSar Server\n"
        "🔴 OFF"
    )


@dp.message(lambda m: m.text == "🖥 Мои серверы")
async def my_servers(message: Message):

    servers = get_servers(
        message.from_user.id
    )

    if not servers:
        await message.answer(
            "У вас нет серверов"
        )
        return

    text = "🖥 Ваши серверы:\n\n"

    for s in servers:
        text += (
            f"ID: {s[0]}\n"
            f"Название: {s[1]}\n"
            f"Статус: {s[2]}\n\n"
        )

    await message.answer(text)


@dp.message(lambda m: m.text == "▶️ Запустить сервер")
async def start(message: Message):

    servers = get_servers(
        message.from_user.id
    )

    if not servers:
        await message.answer(
            "❌ Нет серверов"
        )
        return

    start_server(
        servers[0][0]
    )

    await message.answer(
        "▶️ Сервер запущен"
    )


@dp.message(lambda m: m.text == "⏹ Остановить сервер")
async def stop(message: Message):

    servers = get_servers(
        message.from_user.id
    )

    if not servers:
        await message.answer(
            "❌ Нет серверов"
        )
        return

    stop_server(
        servers[0][0]
    )

    await message.answer(
        "⏹ Сервер остановлен"
    )


@dp.message(lambda m: m.text == "📟 Консоль")
async def console(message: Message):

    result = send_command(
        1,
        "status"
    )

    await message.answer(result)


@dp.message(lambda m: m.text == "🎫 Промокод")
async def promo_button(message: Message):

    await message.answer(
        "🎫 Введите:\n"
        "/promo КОД"
    )


@dp.message(lambda m: m.text == "🆘 Поддержка")
async def support(message: Message):

    await message.answer(
        "🆘 Поддержка PulSar-Host"
    )


@dp.message()
async def other(message: Message):

    await message.answer(
        "Используйте меню 👇"
    )


async def main():

    create_tables()

    print("🚀 PulSar-Host Bot 1.0 запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

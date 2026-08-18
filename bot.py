import asyncio
import os

from aiohttp import web

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

# Новая админ-панель
from admin_panel.panel import router as admin_router

from services.promo import (
    get_promo,
    use_promo
)

from services.servers import (
    create_server,
    user_servers
)

from services.server_manager import (
    start,
    stop,
    restart
)

from services.console import (
    execute_command
)

from services.plans import get_plan

from keyboard import (
    main_menu,
    plans_menu
)


bot = Bot(
    token=BOT_TOKEN
)

dp = Dispatcher()

# Подключаем админ-панель
dp.include_router(
    admin_router
)


@dp.message(Command("start"))
async def start_command(message: Message):

    add_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "🚀 PulSar-Host 1.0\n\n"
        "🎮 Игровой хостинг в Telegram\n\n"
        "Выберите действие 👇",
        reply_markup=main_menu
    )


@dp.message(lambda m: m.text == "👤 Профиль")
async def profile(message: Message):

    await message.answer(
        "👤 Профиль\n\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"💰 Баланс: {get_balance(message.from_user.id)}₽"
    )


@dp.message(lambda m: m.text == "💰 Баланс")
async def balance(message: Message):

    await message.answer(
        f"💰 Баланс: {get_balance(message.from_user.id)}₽"
    )@dp.message(lambda m: m.text == "🛒 Купить сервер")
async def buy_menu(message: Message):

    await message.answer(
        "🛒 Выберите тариф:",
        reply_markup=plans_menu
    )


@dp.message(lambda m: m.text == "🟢 START - 50₽")
async def buy_start(message: Message):

    await buy_plan(
        message,
        "START"
    )


@dp.message(lambda m: m.text == "🔵 PRO - 100₽")
async def buy_pro(message: Message):

    await buy_plan(
        message,
        "PRO"
    )


@dp.message(lambda m: m.text == "🟣 ULTRA - 500₽")
async def buy_ultra(message: Message):

    await buy_plan(
        message,
        "ULTRA"
    )



async def buy_plan(message: Message, plan_name: str):

    plan = get_plan(
        plan_name
    )

    money = get_balance(
        message.from_user.id
    )


    if money < plan["price"]:

        await message.answer(
            "❌ Недостаточно средств\n\n"
            f"Нужно: {plan['price']}₽"
        )

        return


    add_balance(
        message.from_user.id,
        -plan["price"]
    )


    create_server(
        message.from_user.id,
        f"PulSar {plan_name}",
        plan_name
    )


    await message.answer(
        "✅ Сервер создан!\n\n"
        f"📦 Тариф: {plan_name}\n"
        f"💾 RAM: {plan['ram']}\n"
        f"⚙ CPU: {plan['cpu']}\n"
        "⏳ Срок: 30 дней",
        reply_markup=main_menu
    )



@dp.message(lambda m: m.text == "🖥 Мои серверы")
async def servers(message: Message):

    data = user_servers(
        message.from_user.id
    )


    if not data:

        await message.answer(
            "❌ Серверов нет"
        )

        return


    text = "🖥 Ваши серверы:\n\n"


    for s in data:

        text += (
            f"🆔 ID: {s[0]}\n"
            f"📌 {s[1]}\n"
            f"📦 Тариф: {s[2]}\n"
            f"⚡ Статус: {s[3]}\n\n"
        )


    await message.answer(
        text
    )@dp.message(lambda m: m.text == "▶️ Запустить сервер")
async def start_server(message: Message):

    servers = user_servers(
        message.from_user.id
    )

    if not servers:
        await message.answer(
            "❌ Нет серверов"
        )
        return


    await message.answer(
        start(servers[0][0])
    )



@dp.message(lambda m: m.text == "⏹ Остановить сервер")
async def stop_server(message: Message):

    servers = user_servers(
        message.from_user.id
    )

    if not servers:
        await message.answer(
            "❌ Нет серверов"
        )
        return


    await message.answer(
        stop(servers[0][0])
    )



@dp.message(lambda m: m.text == "🔄 Перезапустить сервер")
async def restart_server(message: Message):

    servers = user_servers(
        message.from_user.id
    )

    if not servers:
        await message.answer(
            "❌ Нет серверов"
        )
        return


    await message.answer(
        restart(servers[0][0])
    )



@dp.message(Command("promo"))
async def promo(message: Message):

    args = message.text.split()

    if len(args) < 2:

        await message.answer(
            "Используйте:\n/promo КОД"
        )
        return


    data = get_promo(
        args[1]
    )

    if not data:

        await message.answer(
            "❌ Промокод не найден"
        )
        return


    add_balance(
        message.from_user.id,
        data[1]
    )


    use_promo(
        args[1]
    )


    await message.answer(
        f"✅ Получено +{data[1]}₽"
    )



@dp.message()
async def other(message: Message):

    await message.answer(
        "Используйте меню 👇"
    )



# ===== Render Web Server =====

async def health(request):

    return web.Response(
        text="PulSar-Host Bot is running 🚀"
    )



async def start_web():

    app = web.Application()

    app.router.add_get(
        "/",
        health
    )


    runner = web.AppRunner(app)

    await runner.setup()


    port = int(
        os.getenv(
            "PORT",
            10000
        )
    )


    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )


    await site.start()



async def main():

    create_tables()

    print(
        "🚀 PulSar-Host Bot запущен"
    )


    await start_web()

    await dp.start_polling(
        bot
    )



if __name__ == "__main__":

    asyncio.run(
        main()
    )

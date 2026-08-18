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
    user_servers
)

from services.plans import get_plan

from keyboard import (
    main_menu,
    plans_menu
)


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
        "🚀 PulSar-Host 1.0\n\n"
        "🎮 Игровой хостинг через Telegram\n\n"
        "Выберите действие:",
        reply_markup=main_menu
    )


@dp.message(lambda m: m.text == "💰 Баланс")
async def balance(message: Message):

    money = get_balance(
        message.from_user.id
    )

    await message.answer(
        f"💰 Ваш баланс: {money}₽"
    )


@dp.message(lambda m: m.text == "👤 Профиль")
async def profile(message: Message):

    await message.answer(
        "👤 Профиль\n\n"
        f"ID: {message.from_user.id}\n"
        f"💰 Баланс: {get_balance(message.from_user.id)}₽"
    )


@dp.message(lambda m: m.text == "🛒 Купить сервер")
async def buy_menu(message: Message):

    await message.answer(
        "🛒 Выберите тариф:",
        reply_markup=plans_menu
    )


@dp.message(lambda m: m.text == "🟢 START - 50₽")
async def start_plan(message: Message):

    await buy_plan(
        message,
        "START"
    )


@dp.message(lambda m: m.text == "🔵 PRO - 100₽")
async def pro_plan(message: Message):

    await buy_plan(
        message,
        "PRO"
    )


@dp.message(lambda m: m.text == "🟣 ULTRA - 500₽")
async def ultra_plan(message: Message):

    await buy_plan(
        message,
        "ULTRA"
    )


async def buy_plan(message, plan_name):

    plan = get_plan(plan_name)

    balance = get_balance(
        message.from_user.id
    )


    if balance < plan["price"]:

        await message.answer(
            "❌ Недостаточно средств\n\n"
            f"Цена: {plan['price']}₽\n"
            f"Баланс: {balance}₽"
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
        "⏳ Срок: 30 дней"
    )



@dp.message(lambda m: m.text == "🖥 Мои серверы")
async def servers(message: Message):

    data = user_servers(
        message.from_user.id
    )


    if not data:

        await message.answer(
            "🖥 У вас нет серверов"
        )

        return


    text = "🖥 Ваши серверы:\n\n"


    for s in data:

        text += (
            f"🆔 ID: {s[0]}\n"
            f"📌 Название: {s[1]}\n"
            f"📦 Тариф: {s[2]}\n"
            f"⚡ Статус: {s[3]}\n"
            f"📅 Создан: {s[4]}\n"
            f"⏳ Осталось дней: {s[5]}\n\n"
        )


    await message.answer(text)



@dp.message(Command("promo"))
async def promo(message: Message):

    args = message.text.split()

    if len(args) < 2:
        await message.answer(
            "🎫 Использование:\n/promo КОД"
        )
        return


    code = args[1]

    data = get_promo(code)


    if not data:

        await message.answer(
            "❌ Промокод не найден"
        )

        return


    add_balance(
        message.from_user.id,
        data[1]
    )


    use_promo(code)


    await message.answer(
        f"✅ Промокод активирован!\n"
        f"💰 +{data[1]}₽"
    )



@dp.message(lambda m: m.text == "🎫 Промокод")
async def promo_button(message: Message):

    await message.answer(
        "🎫 Введите:\n/promo КОД"
    )



@dp.message(lambda m: m.text == "⬅️ Назад")
async def back(message: Message):

    await message.answer(
        "Главное меню",
        reply_markup=main_menu
    )



@dp.message(lambda m: m.text == "🆘 Поддержка")
async def support(message: Message):

    await message.answer(
        "🆘 Поддержка PulSar-Host\n"
        "Опишите проблему."
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

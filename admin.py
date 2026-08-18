from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMIN_ID

from database import (
    connect,
    add_balance
)

from services.promo import create_promo
from services.servers import create_server


router = Router()


def is_admin(user_id: int):
    return user_id == ADMIN_ID



@router.message(Command("admin"))
async def admin_panel(message: Message):

    if not is_admin(message.from_user.id):

        await message.answer(
            "❌ Нет доступа"
        )
        return


    await message.answer(
        "🛡 PulSar-Host Admin Panel\n\n"

        "Команды:\n\n"

        "🎫 Создать промокод:\n"
        "/createpromo КОД СУММА КОЛИЧЕСТВО\n\n"

        "💰 Выдать баланс:\n"
        "/givebalance ID СУММА\n\n"

        "🖥 Выдать сервер:\n"
        "/giveserver ID ТАРИФ\n\n"

        "📊 Статистика:\n"
        "/stats"
    )



@router.message(Command("createpromo"))
async def createpromo(message: Message):

    if not is_admin(message.from_user.id):
        return


    args = message.text.split()


    if len(args) < 4:

        await message.answer(
            "Формат:\n"
            "/createpromo КОД СУММА КОЛИЧЕСТВО\n\n"
            "Пример:\n"
            "/createpromo PULSAR100 100 20"
        )

        return


    code = args[1]
    amount = int(args[2])
    limit = int(args[3])


    create_promo(
        code,
        amount,
        limit
    )


    await message.answer(
        "✅ Промокод создан\n\n"
        f"🎫 Код: {code}\n"
        f"💰 Сумма: {amount}₽\n"
        f"👥 Использований: {limit}"
    )



@router.message(Command("givebalance"))
async def givebalance(message: Message):

    if not is_admin(message.from_user.id):
        return


    args = message.text.split()


    if len(args) < 3:

        await message.answer(
            "Формат:\n"
            "/givebalance ID СУММА"
        )

        return


    user_id = int(args[1])
    amount = int(args[2])


    add_balance(
        user_id,
        amount
    )


    await message.answer(
        "✅ Баланс выдан\n\n"
        f"👤 ID: {user_id}\n"
        f"💰 +{amount}₽"
    )



@router.message(Command("giveserver"))
async def giveserver(message: Message):

    if not is_admin(message.from_user.id):
        return


    args = message.text.split()


    if len(args) < 3:

        await message.answer(
            "Формат:\n"
            "/giveserver ID ТАРИФ\n\n"
            "Пример:\n"
            "/giveserver 123456 PRO"
        )

        return


    user_id = int(args[1])
    plan = args[2]


    create_server(
        user_id,
        f"PulSar {plan}",
        plan
    )


    await message.answer(
        "✅ Сервер выдан\n\n"
        f"👤 ID: {user_id}\n"
        f"📦 Тариф: {plan}"
    )



@router.message(Command("stats"))
async def stats(message: Message):

    if not is_admin(message.from_user.id):
        return


    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    users = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM servers"
    )

    servers = cursor.fetchone()[0]


    conn.close()


    await message.answer(
        "📊 PulSar-Host статистика\n\n"
        f"👤 Пользователей: {users}\n"
        f"🖥 Серверов: {servers}"
    )

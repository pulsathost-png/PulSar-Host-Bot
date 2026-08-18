from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMIN_ID
from database import connect, add_balance
from services.promo import create_promo


router = Router()


def is_admin(user_id):
    return user_id == ADMIN_ID



@router.message(Command("admin"))
async def admin(message: Message):

    if not is_admin(message.from_user.id):
        await message.answer(
            "❌ Нет доступа"
        )
        return


    await message.answer(
        "🛡 PulSar-Host Admin Panel\n\n"

        "Команды:\n\n"

        "📊 /stats\n"
        "👥 /users\n"
        "🖥 /servers\n"
        "💰 /give ID СУММА\n"
        "🎫 /promo_create КОД СУММА КОЛ-ВО"
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
        f"👥 Пользователи: {users}\n"
        f"🖥 Серверы: {servers}"
    )



@router.message(Command("users"))
async def users(message: Message):

    if not is_admin(message.from_user.id):
        return


    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT id, username FROM users LIMIT 20"
    )

    data = cursor.fetchall()

    conn.close()


    text = "👥 Пользователи:\n\n"


    for u in data:

        text += (
            f"🆔 {u[0]}\n"
            f"👤 @{u[1]}\n\n"
        )


    await message.answer(text)



@router.message(Command("servers"))
async def servers(message: Message):

    if not is_admin(message.from_user.id):
        return


    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT id,name,plan,status FROM servers"
    )


    data = cursor.fetchall()

    conn.close()


    text = "🖥 Серверы:\n\n"


    for s in data:

        text += (
            f"ID: {s[0]}\n"
            f"📌 {s[1]}\n"
            f"📦 {s[2]}\n"
            f"⚡ {s[3]}\n\n"
        )


    await message.answer(text)



@router.message(Command("give"))
async def give(message: Message):

    if not is_admin(message.from_user.id):
        return


    args = message.text.split()


    if len(args) != 3:

        await message.answer(
            "Формат:\n"
            "/give ID СУММА"
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
        f"👤 {user_id}\n"
        f"💰 +{amount}₽"
    )



@router.message(Command("promo_create"))
async def promo_create(message: Message):

    if not is_admin(message.from_user.id):
        return


    args = message.text.split()


    if len(args) != 4:

        await message.answer(
            "Формат:\n"
            "/promo_create КОД СУММА КОЛ-ВО"
        )

        return


    create_promo(
        args[1],
        int(args[2]),
        int(args[3])
    )


    await message.answer(
        "🎫 Промокод создан!"
    )

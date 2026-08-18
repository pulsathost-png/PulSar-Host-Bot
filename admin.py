from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMIN_ID

from database import (
    connect,
    add_balance
)

from services.promo import create_promo

from admin_keyboard import admin_menu


router = Router()


def is_admin(user_id):
    return user_id == ADMIN_ID



# Открытие админки

@router.message(Command("admin"))
async def admin(message: Message):

    if not is_admin(message.from_user.id):

        await message.answer(
            "❌ Нет доступа"
        )

        return


    await message.answer(
        "🛡 PulSar-Host Admin Panel",
        reply_markup=admin_menu
    )



# Статистика

async def stats(message: Message):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    users_count = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM servers"
    )

    servers_count = cursor.fetchone()[0]


    conn.close()


    await message.answer(
        "📊 Статистика PulSar-Host\n\n"
        f"👥 Пользователи: {users_count}\n"
        f"🖥 Серверы: {servers_count}"
    )



@router.message(Command("stats"))
async def stats_command(message: Message):

    if is_admin(message.from_user.id):
        await stats(message)



# Пользователи

async def users(message: Message):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT id, username FROM users LIMIT 20"
    )

    data = cursor.fetchall()

    conn.close()


    text = "👥 Пользователи:\n\n"


    for user in data:

        text += (
            f"🆔 ID: {user[0]}\n"
            f"👤 @{user[1]}\n\n"
        )


    await message.answer(text)



@router.message(Command("users"))
async def users_command(message: Message):

    if is_admin(message.from_user.id):
        await users(message)



# Серверы

async def servers(message: Message):

    conn = connect()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT id,name,plan,status FROM servers"
    )

    data = cursor.fetchall()

    conn.close()


    text = "🖥 Серверы:\n\n"


    for server in data:

        text += (
            f"🆔 ID: {server[0]}\n"
            f"📌 {server[1]}\n"
            f"📦 {server[2]}\n"
            f"⚡ {server[3]}\n\n"
        )


    await message.answer(text)



@router.message(Command("servers"))
async def servers_command(message: Message):

    if is_admin(message.from_user.id):
        await servers(message)



# Выдача баланса

@router.message(Command("give"))
async def give(message: Message):

    if not is_admin(message.from_user.id):
        return


    args = message.text.split()


    if len(args) != 3:

        await message.answer(
            "Использование:\n"
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
        f"👤 ID: {user_id}\n"
        f"💰 +{amount}₽"
    )



# Создание промокода

@router.message(Command("promo_create"))
async def promo_create(message: Message):

    if not is_admin(message.from_user.id):
        return


    args = message.text.split()


    if len(args) != 4:

        await message.answer(
            "Формат:\n"
            "/promo_create КОД СУММА КОЛИЧЕСТВО"
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



# Кнопки админки

@router.message(lambda m: m.text == "📊 Статистика")
async def stats_button(message: Message):

    if is_admin(message.from_user.id):
        await stats(message)



@router.message(lambda m: m.text == "👥 Пользователи")
async def users_button(message: Message):

    if is_admin(message.from_user.id):
        await users(message)



@router.message(lambda m: m.text == "🖥 Серверы")
async def servers_button(message: Message):

    if is_admin(message.from_user.id):
        await servers(message)



@router.message(lambda m: m.text == "⬅️ Выйти из админки")
async def exit_admin(message: Message):

    await message.answer(
        "✅ Вы вышли из админ-панели"
        )

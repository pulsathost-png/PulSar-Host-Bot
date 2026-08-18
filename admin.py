from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMIN_ID
from services.promo import create_promo
from database import connect, add_balance


router = Router()


def is_admin(user_id):
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
        "🎫 /createpromo\n"
        "💰 /givebalance\n"
        "📊 /stats"
    )


@router.message(Command("createpromo"))
async def createpromo(message: Message):

    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🎫 Создание промокода:\n\n"
        "Формат:\n"
        "КОД СУММА КОЛИЧЕСТВО\n\n"
        "Пример:\n"
        "PULSAR100 100 20"
    )


@router.message(Command("givebalance"))
async def givebalance(message: Message):

    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "💰 Выдача денег:\n\n"
        "Формат:\n"
        "ID СУММА\n\n"
        "Пример:\n"
        "123456789 500"
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

    conn.close()

    await message.answer(
        f"📊 Статистика PulSar-Host\n\n"
        f"👥 Пользователей: {users}"
    )


@router.message()
async def admin_actions(message: Message):

    if not is_admin(message.from_user.id):
        return

    text = message.text.split()

    # создание промокода
    if len(text) == 3:

        code = text[0]
        amount = int(text[1])
        uses = int(text[2])

        create_promo(
            code,
            amount,
            uses
        )

        await message.answer(
            "✅ Промокод создан!"
    )

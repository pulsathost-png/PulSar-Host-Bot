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

        "🎫 Создать промокод:\n"
        "/createpromo\n\n"

        "💰 Выдать баланс:\n"
        "/givebalance\n\n"

        "🖥 Выдать сервер:\n"
        "/giveserver\n\n"

        "📊 Статистика:\n"
        "/stats"
    )



# =========================
# ПРОМОКОДЫ
# =========================


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



# =========================
# ВЫДАЧА БАЛАНСА
# =========================


@router.message(Command("givebalance"))
async def givebalance(message: Message):

    if not is_admin(message.from_user.id):
        return


    await message.answer(
        "💰 Выдача баланса:\n\n"

        "Формат:\n"
        "ID СУММА\n\n"

        "Пример:\n"
        "123456789 500"
    )



# =========================
# ВЫДАЧА СЕРВЕРА
# =========================


@router.message(Command("giveserver"))
async def giveserver(message: Message):

    if not is_admin(message.from_user.id):
        return


    await message.answer(
        "🖥 Выдача сервера:\n\n"

        "Формат:\n"
        "ID ТАРИФ\n\n"

        "Пример:\n"
        "123456789 PRO"
    )



# =========================
# СТАТИСТИКА
# =========================


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

        f"👥 Пользователей: {users}\n"
        f"🖥 Серверов: {servers}"
    )



# =========================
# ОБРАБОТКА ДАННЫХ АДМИНА
# =========================


@router.message()
async def admin_actions(message: Message):

    if not is_admin(message.from_user.id):
        return


    args = message.text.split()



    # Создание промокода
    # PULSAR100 100 20

    if len(args) == 3:

        try:

            code = args[0]
            amount = int(args[1])
            uses = int(args[2])


            create_promo(
                code,
                amount,
                uses
            )


            await message.answer(
                "✅ Промокод создан!\n\n"

                f"🎫 Код: {code}\n"
                f"💰 Бонус: {amount}₽\n"
                f"🔢 Использований: {uses}"
            )


        except:
            pass



    # Выдача баланса
    # 123456789 500

    elif len(args) == 2:

        try:

            user_id = int(args[0])
            amount = int(args[1])


            add_balance(
                user_id,
                amount
            )


            await message.answer(
                "✅ Баланс выдан!\n\n"

                f"👤 ID: {user_id}\n"
                f"💰 Сумма: {amount}₽"
            )


        except:
            pass

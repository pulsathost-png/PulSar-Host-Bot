from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMIN_ID
from services.promo import create_promo

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У тебя нет доступа.")
        return

    await message.answer(
        "🛡 PulSar-Host Admin Panel\n\n"
        "Команды:\n"
        "/createpromo - создать промокод\n"
        "/stats - статистика"
    )


@router.message(Command("createpromo"))
async def create_promo_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "Введите промокод в формате:\n\n"
        "КОД СУММА КОЛИЧЕСТВО\n\n"
        "Пример:\n"
        "PULSAR50 50 10"
    )


@router.message()
async def promo_create_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.split()

    if len(text) == 3:
        code = text[0]
        amount = int(text[1])
        uses = int(text[2])

        create_promo(code, amount, uses)

        await message.answer(
            f"✅ Промокод создан!\n\n"
            f"🎫 Код: {code}\n"
            f"💰 Бонус: {amount}₽\n"
            f"🔢 Использований: {uses}"
        )

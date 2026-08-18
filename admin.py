from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMIN_ID

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У тебя нет доступа к админ-панели.")
        return

    await message.answer(
        "🛡 PulSar-Host Admin Panel\n\n"
        "Доступные функции:\n"
        "💰 Выдать баланс\n"
        "🎫 Создать промокод\n"
        "🖥 Выдать сервер\n"
        "📊 Статистика"
    )

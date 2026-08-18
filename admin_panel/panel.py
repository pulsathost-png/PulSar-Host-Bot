from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMIN_ID
from admin_keyboard import admin_menu


router = Router()


def is_admin(user_id: int):
    return user_id == ADMIN_ID



@router.message(Command("admin"))
async def open_admin_panel(message: Message):

    if not is_admin(message.from_user.id):

        await message.answer(
            "❌ Доступ запрещён"
        )
        return


    await message.answer(
        "🛡 PulSar-Host Admin Panel\n\n"
        "Добро пожаловать в панель управления 👑",
        reply_markup=admin_menu
    )

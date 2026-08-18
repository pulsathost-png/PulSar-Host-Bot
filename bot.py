import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from config import BOT_TOKEN
from database import create_tables


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🚀 Добро пожаловать в PulSar-Host!\n\n"
        "🎮 Игровой хостинг через Telegram\n"
        "Версия: 1.0"
    )


@dp.message()
async def message_handler(message: Message):
    await message.answer(
        "Используй команду /start"
    )


async def main():
    create_tables()
    print("PulSar-Host Bot запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

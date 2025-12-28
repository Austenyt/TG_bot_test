import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = '8354942786:AAEjBj-INmHEUmRdHZ9wR1WOj0xu51raVyo'

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer('Привет! Введите координаты')


@dp.message(Command('Прогноз'))
async def weather_command(message: Message):
    await message.answer('Введите координаты!')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')

import asyncio
import geocoder

from aiogram import Bot, Dispatcher
from aiogram.client.session import aiohttp
from aiogram.filters import CommandStart
from aiogram.types import Message

with open('.env', 'r') as file:
    for line in file:
        if line.startswith('TOKEN='):
            TOKEN = line.strip().split('=')[1]
            break
        else:
            raise ValueError("Токен не найден в файле .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer('Привет! Введите название города')


@dp.message()
async def weather_command(message: Message):
    try:
        g = geocoder.osm(message.text, reverse=True)
    except KeyError:
        await message.answer(f'Город не найден')
        return None
    print(g.latlng)
    print(g.city)

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.open-meteo.com/v1/forecast?latitude={g.lat}&longitude={g.lng}&current'
                               '=temperature_2m,wind_speed_10m') as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            content = await response.json()
            if response.status != 200:
                await message.answer("Указанный город не найден")
            print(content)
            temp = content['current']['temperature_2m']
            wind = content['current']['wind_speed_10m']
            await message.answer(f'Температура в {g.city} составляет: {temp}\n'
                                 f'Скорость ветра в {g.city} составляет: {wind}')


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')

# @dp.message()
# async def weather_command(message: Message):
#     text = message.text.strip().rstrip()
#     while '  ' in text:
#         text = text.replace('  ', ' ')
#     coordinates = text.split(', ')
#     if len(coordinates) != 2:
#         await message.answer('Введите координаты в нужном формате!')
#         return None
#     lat, long = coordinates
#     async with aiohttp.ClientSession() as session:
#         async with session.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current'
#                                '=temperature_2m,wind_speed_10m') as response:
#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])
#
#             content = await response.json()
#             temp = content['current']['temperature_2m']
#             wind = content['current']['wind_speed_10m']
#             await message.answer(f'Температура в указанных координатах составляет: {temp}\n'
#                                  f'Скорость ветра в указанных координатах составляет: {wind}')
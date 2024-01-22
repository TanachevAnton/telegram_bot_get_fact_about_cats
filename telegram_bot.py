import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from telegram_bot_get_fact_about_cats.get_cat_fact import URL, URL_PHOTO, cats_fact, get_cat_photo

ABOUT_BOT_BTN = 'О боте'
GET_CATS_FACT_BTN = 'Запросить факт'

bot = Bot(token=getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    buttons = [
        [KeyboardButton(text=GET_CATS_FACT_BTN)],
        [KeyboardButton(text=ABOUT_BOT_BTN)]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие'
    )
    await message.answer(
        text=f'Привет! Я бот, который будет тебя знакомить с фактами о кошках! '
             f'Отправь мне любое сообщение, а я пришлю тебе какой-нибудь факт.',
        reply_markup=keyboard
    )

@dp.message(F.text == ABOUT_BOT_BTN)
async def about_bot_info(message: types.Message):
    await message.reply(
        f'Данный бот забирает данные из открытого источника по API {URL}.\n\n'
        f'Бот получает ответ GET-запросом, переводит его на русский язык с помощью google-переводчика, '
        f'и вы получаете ответ в виде одного факта о котах =)\n\n'
        f'Ниже вы можете видеть json-файл - это результат выполнения запроса по API на указанный выше сервис.'
    )

@dp.message(F.text == GET_CATS_FACT_BTN)
async def get_cats_fact(message: types.Message):
    result = str(cats_fact())
    photo_path = str(get_cat_photo(URL_PHOTO))
    print(photo_path)
    await message.reply(result)
    await bot.send_photo(chat_id=message.chat.id, photo=photo_path)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked

from aiogram.dispatcher.filters import Text

import inline_keyboard
import messages

logging.basicConfig(level=logging.INFO)

bot_api_token = '5423666614:AAHL5Wf64WZziSamjVUE5S7kQg2a14Eg3D8'
# Объект бота
bot = Bot(token=bot_api_token)
# Диспетчер для бота
dp = Dispatcher(bot)

# Хэндлер на команду /start
@dp.message_handler(commands='start')
async def start_menu(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}.\nС чего начнем?',
                        reply_markup=inline_keyboard.keyboard)


@dp.message_handler(Text(equals='Улучшить фото'))
async def get_photo_to_upscale(message: types.Message):
    await message.answer('Отправь мне фото, которое хочешь улучшить')


@dp.message_handler(Text(equals='Стилизовать фото'))
async def get_photo_to_stylize(message: types.Message):
    await message.answer('Отправь мне фото, которое хочешь стилизовать')


@dp.message_handler(Text(equals='Убрать фон с фото'))
async def get_photo_to_delete_bg(message: types.Message):
    await message.answer('Отправь мне фото, с которого хочешь убрать фон')


@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    await message.photo[-1].download('img')
    await message.answer('А теперь отправь стиль, в котором ты хочешь сделать фото')


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import asyncio
import logging
import datetime
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils import States

from aiogram.dispatcher.filters import Text

import inline_keyboard
import bd

logging.basicConfig(level=logging.INFO)

downloads_photo_directory = 'C:/Users/Egor/PycharmProjects/CourseWork(5 term)/img/photo'
downloads_style_directory = 'C:/Users/Egor/PycharmProjects/CourseWork(5 term)/img/style'
done_img = 'C:/Users/Egor/PycharmProjects/CourseWork(5 term)/best.png'

bot_api_token = '5423666614:AAHL5Wf64WZziSamjVUE5S7kQg2a14Eg3D8'
# Объект бота
bot = Bot(token=bot_api_token)
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())


# Хэндлер на команду /start
@dp.message_handler(commands='start')
async def start_menu(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}.\nС чего начнем?',
                         reply_markup=inline_keyboard.keyboard)
    user_id = message.from_user.id
    print(user_id)
    bd.execute_query(bd.create_connection, bd.add_user_query)

@dp.message_handler(Text(equals='Улучшить фото'))
async def get_photo_to_upscale(message: types.Message):
    await message.answer('Отправь мне фото, которое хочешь улучшить')


@dp.message_handler(Text(equals='Стилизовать фото'))
async def get_photo_to_stylize(message: types.Message):
    await message.answer(text='Так-с...',
                         reply_markup=inline_keyboard.keyboard_photo)


@dp.message_handler(Text(equals='Убрать фон с фото'))
async def get_photo_to_delete_bg(message: types.Message):
    await message.answer('Отправь мне фото, с которого хочешь убрать фон')


@dp.message_handler(Text(equals='Отправить фото'))
async def set_wait_content_state(message: types.Message):
    await message.answer("Отправь фото:")
    await States.WAIT_PHOTO_STATE.set()   # Set state


@dp.message_handler(Text(equals='Отправить стиль'))
async def set_wait_style_state(message: types.Message):
    await message.answer("Отправь стиль для фото:")
    await States.WAIT_STYLE_STATE.set()


@dp.message_handler(state=States.WAIT_PHOTO_STATE, content_types=types.ContentTypes.PHOTO)
async def get_photo(message: types.Message, state: FSMContext):
    photo_abspath = '{}/photos/{}.jpg'.format(downloads_photo_directory, datetime.datetime.now().strftime(
        "%Y%m%d-%H%M%S-%f"))  # Downloaded photo path to downloads/photos
    user_id = message.from_user.id
    print(user_id)

    content_id = message.photo[-1].file_id
    content_info = await bot.get_file(content_id)
    path = content_info.file_path
    await bot.download_file(path, photo_abspath)
    await state.finish()

    print(photo_abspath)

    await message.answer('Получил твое фото😉', reply_markup=inline_keyboard.keyboard)
    bd.execute_query(bd.create_connection, bd.add_content_query)
    #return photo_abspath


@dp.message_handler(state=States.WAIT_STYLE_STATE, content_types=types.ContentTypes.PHOTO)
async def get_photo_style(message: types.Message, state: FSMContext):
    style_abspath = '{}/photos/{}.jpg'.format(downloads_style_directory, datetime.datetime.now().strftime(
        "%Y%m%d-%H%M%S-%f"))  # Downloaded photo path to downloads/photos

    style_id = message.photo[-1].file_id
    style_info = await bot.get_file(style_id)
    style_path = style_info.file_path
    await bot.download_file(style_path, style_abspath)
    await state.finish()

    print(style_abspath)
    await message.answer('Получил твое фото😉', reply_markup=inline_keyboard.stylish_level_keyboard)
    bd.execute_query(bd.create_connection, bd.add_style_query)

@dp.message_handler(Text(equals='Составить изображение'))
async def compute(message: types.Message):
    await bot.send_message(chat_id='486325118', text='Выберите уровень стилизации\n'
                                                     '1 - Слабый уровень стилизации\n'
                                                     '2 - Средний уровень стилизации\n'
                                                    '3 - Хороший уровень стилизации\n'
                                                    '4 - Высокий уровень стилизации')
    await bot.send_photo(message.chat.id, done_img)

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

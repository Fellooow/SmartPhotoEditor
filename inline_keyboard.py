from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Making buttons
upscale_button = KeyboardButton('Улучшить фото')
stylize_photo_button = KeyboardButton('Стилизовать фото')
delete_bg_button = KeyboardButton('Убрать фон с фото')

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(upscale_button, stylize_photo_button, delete_bg_button)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Making buttons
upscale_button = KeyboardButton('Улучшить фото')
stylize_photo_button = KeyboardButton('Стилизовать фото')
delete_bg_button = KeyboardButton('Убрать фон с фото')


# Buttons to work with images
send_photo = KeyboardButton('Отправить фото', callback_data='get_photo')
send_style = KeyboardButton('Отправить стиль', callback_data='get_photo_style')

# Buttons to set stylish level
button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')
button4 = KeyboardButton('4️⃣')

stylish_level_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
stylish_level_keyboard.add(button1, button2, button3, button4)

keyboard_photo = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_photo.add(send_photo, send_style)


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(upscale_button, stylize_photo_button, delete_bg_button)


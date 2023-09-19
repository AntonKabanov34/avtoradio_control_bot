import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

from config import TOKEN
from clases import db
from texts import welcome, users, no_users, on_air, web_site, valute, admin

API_TOKEN = TOKEN  

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Main Keyboard Button
def main_keyboard_button() -> ReplyKeyboardMarkup:
    """Выводит командную клавиатуру для верефицированных пользователей"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_on_air = KeyboardButton(on_air)
    button_web_site = KeyboardButton(web_site)
    button_valute = KeyboardButton(valute)
    button_admin = KeyboardButton(admin)

    markup.add(button_on_air, button_web_site, button_valute)
    markup.add(button_admin)
    return markup


# Обработчик команд
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Проверка на первого пользователя, создание первого админа
    if db.examination_count_user() == True:
        db.add_data('bot_users', message.from_user.id, message.from_user.first_name, 
                    message.from_user.username, 1, 0, None)
        await bot.send_message(message.chat.id, welcome)
        pass
    
    # Логинг пользователей, для доступа к функционалу
    elif db.examination_count_user() == False:
        # Логируем пользователя
        if db.loging_users(message.from_user.id):
            await bot.send_message(message.chat.id, users, reply_markup=main_keyboard_button())
            pass  
        else:
            await bot.send_message(message.chat.id, no_users)
            pass
    
    # На случай если сломается
    else:
        print('Произошла ошибка в обработчике команды START')
        pass

# Обработчик сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text_message(message: types.Message):
    
    # Обработчик команды "Эфир"
    if message.text == on_air:
        if db.loging_users(message.from_user.id):
            await bot.send_message(message.chat.id, 'Вы запросили доступ к эфиру')
            pass
        else:
            await bot.send_message(message.chat.id, no_users)
            pass
    
    # Обработчик команды "Сайт"
    elif message.text == web_site:
        if db.loging_users(message.from_user.id):
            await bot.send_message(message.chat.id, 'Вы запросили подписку на рассылку сайта')
            pass
        else:
            await bot.send_message(message.chat.id, no_users)
            pass

    # Обработчик команды "Валюты"
    elif message.text == valute:
        if db.loging_users(message.from_user.id):
            await bot.send_message(message.chat.id, 'Вы запросили доступ к валютам')
            pass
        else:
            await bot.send_message(message.chat.id, no_users)
            pass
    
    # Обработчик команды "Администратор"
    elif message.text == admin:
        # Проверка на админа
        await bot.send_message(message.chat.id, 'Вы запросили доступ к меню администратора')
        pass

    # На случай если что-то сломается
    else:
        print('Что-то произошло в блоке message_handler, обработчике текстовых команд')
        pass



        












if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

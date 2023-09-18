import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

from config import TOKEN
from clases import db
from texts import welcome, users, no_users

API_TOKEN = TOKEN  

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

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
            await bot.send_message(message.chat.id, users)
            # Добавить сюда принтовку основного меню
            pass  
        else:
            await bot.send_message(message.chat.id, no_users)
            pass
    
    # На случай если сломается
    else:
        print('Произошла ошибка в обработчике команды START')
        pass













if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

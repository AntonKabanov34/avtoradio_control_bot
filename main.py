# Библиотеки
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Модули
from config import TOKEN, folder_b
from clases import db, audio
from texts import welcome, users, no_users, on_air, web_site, valute, admin, \
list_users,list_new_users, what_action, choise_user, new_admin, low_users, del_users, \
yes_new_users, no_new_users, admin_aplikation, yes_aplication, no_aplication, receipt, yes_receipt, goodbay,\
date_folder, time_file


API_TOKEN = TOKEN  

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

admin_responses = [] # Хранит ответы админа
new_users_data = []
user_responses_audio = [] # Хранит запросы пользователя


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

#InlineButton Admin Menu
def admin_main_inline_keyboard() -> InlineKeyboardButton:
    """Кнопки базового меню админа"""
    list_users_button = InlineKeyboardButton(list_users, callback_data = 'list_users')
    new_users_button = InlineKeyboardButton(list_new_users, callback_data = 'new_users')

    keyboard = InlineKeyboardMarkup()
    keyboard.add(list_users_button, new_users_button)

    return keyboard 

def users_inline_list(input_chat_id, table:str) -> InlineKeyboardButton:
    """Выводит список пользователей"""
    users = db.users_list(table)
    buttons = [InlineKeyboardButton(first_name, callback_data=str(chat_id))
           for first_name, chat_id in users.items() if chat_id != input_chat_id]
    
    back_button = InlineKeyboardButton("<- Назад", callback_data="back_main_admin")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons, back_button)
    return markup

def add_users_inline() -> InlineKeyboardButton:
    """Принтует меню админа"""
    do_user_button = InlineKeyboardButton(low_users, callback_data = 'do_user')
    do_superuser_button = InlineKeyboardButton(new_admin, callback_data = 'new_admin')
    dellete_user_button = InlineKeyboardButton(del_users, callback_data = 'dellete_user')

    back_button = InlineKeyboardButton("<- Назад", callback_data="back_main_admin")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(do_user_button, do_superuser_button, dellete_user_button)
    keyboard.add(back_button)

    return keyboard 

def add_new_users_inline() -> InlineKeyboardButton:
    """Кнопки для добавления нового пользователя"""
    yes_user = InlineKeyboardButton(yes_new_users, callback_data = 'yes_new_users')
    no_users = InlineKeyboardButton(no_new_users, callback_data = 'no_new_users')

    back_button = InlineKeyboardButton("<- Назад", callback_data="back_main_admin")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(yes_user, no_users)
    keyboard.add(back_button)

    return keyboard

def new_users_inline() -> InlineKeyboardButton:
    """Отправляет пользователю кнопку заявки"""
    aplication_yes = InlineKeyboardButton(yes_aplication, callback_data = 'aplication_yes')
    aplication_no = InlineKeyboardButton(no_aplication, callback_data = 'aplication_no')   
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(aplication_yes, aplication_no)

    return keyboard 


#Inline Audio Menu
def main_date_audio_inline() -> InlineKeyboardButton:
    """Выводитменю со списокм доступных дат аудио"""
    # получаем словарь
    req = audio.print_dates(folder_b)
    buttons = [InlineKeyboardButton(folder, callback_data=str(req[folder]))
           for folder in req]
    #back_button = InlineKeyboardButton("<- Назад", callback_data="back_main_admin")
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(*buttons)
    return markup

def time_menu_audio_inline() -> InlineKeyboardButton:
    """Выводит список доступных временных слотов"""
    req = audio.print_time_slots(folder_b, user_responses_audio[0])

    buttons = [InlineKeyboardButton(time, callback_data=str(req[time]))
           for time in req]
    back_button = InlineKeyboardButton("<- Назад", callback_data = 'audio_date_menu')
    markup = InlineKeyboardMarkup(row_width=4)
    markup.add(*buttons)
    markup.add(back_button)
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
            db.add_data('new_bot_users', message.from_user.id, message.from_user.first_name, 
                    message.from_user.username, 0, 0, None)
            new_users_data.append(message.from_user.id)
            await bot.send_message(message.chat.id, no_users, reply_markup=new_users_inline())
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
            await bot.send_message(message.chat.id, date_folder, reply_markup = main_date_audio_inline())
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
        if db.admin_users('bot_users', message.chat.id, 1):
            await bot.send_message(message.chat.id, what_action, reply_markup=admin_main_inline_keyboard())
            admin_responses.clear()
            pass
        else:
            await bot.send_message(message.chat.id, no_users)
            pass

    # На случай если что-то сломается
    else:
        print('Что-то произошло в блоке message_handler, обработчике текстовых команд')
        pass

# Обработчик колбеков
@dp.callback_query_handler(lambda callback_query: True)
async def main_callback(query: types.CallbackQuery):

    # Показывает список пользователей
    if query.data == 'list_users':
        admin_responses.clear()
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=choise_user,
            reply_markup=users_inline_list(query.message.chat.id, 'bot_users'))
        admin_responses.append('bot_users')
        pass

     # Показывает список новых пользователей 
    
    # Показывает список заявок
    elif query.data == 'new_users':
        admin_responses.clear()
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=choise_user,
            reply_markup=users_inline_list(query.message.chat.id, 'new_bot_users'))
        admin_responses.append('new_bot_users')
        pass

    # Выводит данные о пользователях    
    elif len(admin_responses) > 0 and query.data in db.user_chat_id(admin_responses[0]):
        admin_responses.append(query.data)
        # Принтуем данные пользователя (мтод в ДБ который принимает таблицу и чат ID)
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=db.print_info_user(admin_responses[0],admin_responses[1]),
            reply_markup = add_users_inline() if admin_responses[0] == 'bot_users' else add_new_users_inline())
        pass

    # Меняет статус пользователя на 0 (юзер) в таблице bot_users    
    elif query.data == 'do_user':
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=db.change_users(admin_responses[0],admin_responses[1], query.data))
        admin_responses.clear()
        pass
    
    # Меняет статус пользователя на 1 (суперюзер) в таблице bot_users
    elif query.data == 'new_admin':
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=db.change_users(admin_responses[0], admin_responses[1], query.data))
        admin_responses.clear()
        pass

    # Удаляет пользователя из таблицы bot_users
    elif query.data == 'dellete_user':
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=db.change_users(admin_responses[0], admin_responses[1], query.data))
        admin_responses.clear()
        pass

    # Переносит пользователя из таблицы new_bot_users в таблицу bot_users
    elif query.data == 'yes_new_users':
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text= db.change_users(admin_responses[0], admin_responses[1], query.data))
        await bot.send_message(admin_responses[1], yes_receipt)
        admin_responses.clear()
        pass

    # Удаляет пользователя из таблицы new_bot_users
    elif query.data == 'no_new_users':
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text= db.change_users(admin_responses[0], admin_responses[1], 'dellete_user'))
        admin_responses.clear()
        pass

    #Инлайн - возвращает в меню админа
    elif query.data == 'back_main_admin':
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=what_action,
            reply_markup=admin_main_inline_keyboard())
        pass

    # Отправляет заявку пользователя на доступ к функционалу
    elif query.data == 'aplication_yes':
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=receipt)
        admin = db.chat_id_list('bot_users', 'user_status',1)
        new_users_data.clear()
        for a in admin:
            await bot.send_message(a, admin_aplikation)
        pass

    # Отправляет пользователю заглушку
    elif query.data == 'aplication_no':
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=goodbay)
        db.dellete_users('new_bot_users', new_users_data[0])
        new_users_data.clear()
        pass
    
    # Обработчик запроса даты эфира
    elif query.data in audio.date_list(folder_b):
        """Обрабатывает колбек с кнопуи выбора даты"""
        user_responses_audio.clear()
        user_responses_audio.append(query.data)
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=time_file,
            reply_markup=time_menu_audio_inline())
        pass

    # Обработчик запроса файла эфира
    elif query.data in audio.file_list(folder_b, user_responses_audio[0]):
        user_responses_audio.append(query.data)
        
        date_dict = audio.reverse_dict(audio.print_dates(folder_b))
        tm_slots = audio.reverse_dict(audio.print_time_slots(folder_b, user_responses_audio[0]))
        mess = f'Дата: {date_dict[user_responses_audio[0]]}. Время: {tm_slots[user_responses_audio[1]]}'
        
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=mess)
        file = open(f'{folder_b}/{user_responses_audio[0]}/{user_responses_audio[1]}', 'rb')
        await bot.send_audio(query.message.chat.id, file )
        file.close
        user_responses_audio.clear()
        pass

    #Возвращает пользователя к выбору даты    
    elif query.data == 'audio_date_menu':
        user_responses_audio.clear()
        await bot.edit_message_text(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            text=date_folder,
            reply_markup=main_date_audio_inline())
        pass

    else:
        print('Что-то проищошло при обработке callback')
        pass





if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

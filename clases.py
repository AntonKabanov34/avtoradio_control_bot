# Модули
from config import folder_a, folder_b
from users_rqests_map import mounth
from config import db_name

# Библиотеки
import sqlite3
from os import listdir, path
from shutil import copytree
from datetime import datetime
from re import match
import shutil
import requests

class Audio_file:
    def __init__(self, folder_a: str, folder_b: str):
        """Принимает папку ОТКУДА и КУДА"""
        self.folder_a = folder_a
        self. folder_b = folder_b
        pass
    

    def copy_file(self, folder_a: str, folder_b: str):
        """Зеркалит папку А"""
        list_a = listdir(folder_a)
        list_b = listdir(folder_b)

        pattern_folder_name = r'^\d{4}-\d{2}-\d{2}$'
        pattern_file_name = r'^\d{2}-\d{2}-\d{2}\.mp3$'

        if list_b not in list_a:
            # В начале суток появляется новая папка
            new_folder = [item for item in list_a if item not in list_b]
            print(f'Новые объекты папок: {new_folder}')
            if len(new_folder) > 0:
                for folder_name in new_folder:
                    if match(pattern_folder_name, folder_name):
                        source_folder = path.join(folder_a, folder_name)
                        destination_folder = path.join(folder_b, folder_name)

                        # Копируем папку и её содержимое
                        shutil.copytree(source_folder, destination_folder)
                        print(f'Папка {folder_name} была скопирована в каталог бота')
            else:
                print('Новые папки не обнаружены')
                pass    
        
        
        for folder_name in sorted(list_b):
            if match(pattern_folder_name, folder_name):
                file_name_a = self.file_in_folder(folder_a, folder_name)
                file_name_b = self.file_in_folder(folder_b, folder_name)
                    
                if file_name_b != file_name_a:
                    print(f'В папке {folder_name} есть новые файлы')
                    # Получить список файлов которые отсуттсвуют в папке Б
                    file_name_list = [item for item in file_name_a if item not in file_name_b]

                    print(f'{len(file_name_list)} штук')
                        
                    for file in file_name_list:
                        if match(pattern_file_name, file):
                            # folder_name - папка в которой нашли несоответствие
                            # Путь к папке исходнику 
                            file_path_a = f'{folder_a}/{folder_name}/{file}'
                            folder_path_b = f'{folder_b}/{folder_name}'

                            # Копируем папку и её содержимое
                            shutil.copy2(file_path_a, folder_path_b)
                            print(f'Файл {file} был скопирована в каталог бота')
                        else:
                            print(f'При копировании файлов, поймали какое-то странное имя:{file}')
                            pass
        print ('Все новые объекты были скопированы в каталог бота')
        pass    

    def dellete_audio_folders(self, folder_b: object):
        """Удалят старые папки"""
        len_folders = 5
        pattern_folder_name = r'^\d{4}-\d{2}-\d{2}$'

        folder_list = []
        for i in listdir(folder_b):
            if match(pattern_folder_name, i):
                folder_list.append(i)
            else:
                pass
        sorted(folder_list)
        print(folder_list)

        
        while len(folder_list) > len_folders:
            folder_path = f'{folder_b}/{folder_list[0]}'
            if path.exists(folder_path):  # Проверяем существование папки
                try:
                    shutil.rmtree(folder_path)
                    print(f'Папка {folder_path} и её содержимое были успешно удалены.')
                except OSError as e:
                    print(f'Ошибка при удалении папки и её содержимого: {e}')
            else:
                print(f'Папка {folder_path} не существует.')
            
            folder_list.pop(0)

    def file_in_folder(self, folder_path, folder:str) -> list:
        """Принимает имя каталога и имя папки, возвращает список файлов в папке"""
        folder_path = f'{folder_path}/{folder}'
        file_names = [file_name for file_name in listdir(folder_path) if path.isfile(path.join(folder_path, file_name))]   
        return file_names

    def available_dates(self, folder: str) -> list:
        """Формирует список доступных дат архива"""
        folders_default = listdir(folder)
        folders =[]
        for folder in folders_default:
            if folder != '.DS_Store':
                folders.append(folder)
            else:
                pass
        return folders
        pass
    
    def print_available_dates(self, folder: list) -> dict:
        """Формирует для пользователя список доступных дат"""
        # {'15 Февраля': 2022-02-15}
        date_dict = {}
        for date_obj in folder:
            date = datetime.strptime(date_obj, "%Y-%m-%d")
            month_number = date.month
            add_key = f'{date.day} {mounth[month_number]}'
            date_dict[add_key] = date_obj
        return date_dict
        pass


    def print_available_airs(self):
        """Формирует для пользователя словарь с доступными записями эфира"""
        pass
        

class DataBase:
    def __init__(self, db_name: str):
        """Получает на вход только имя БД"""
        self.db_name = db_name
        pass

    def create_db_users(self):
        """Создает БД при старте"""
        
        # Создаем таблицу bot_users
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bot_users (
                        id INTEGER PRIMARY KEY,
                        chat_id INTEGER,
                        first_name TEXT,
                        username TEXT,
                        user_status INTEGER,
                        news_subscribe INTEGER,
                        last_uid_news INTEGER
                    )
                ''')

            print(f'База данных {self.db_name} инициализирована.')
        except sqlite3.Error as e:
            print(f'База данных не найдена или произошла ошибка: {e}')

        # Создаем таблицу user_count
        try:
            with sqlite3.connect(db_name) as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_counts (
                        id INTEGER PRIMARY KEY,
                        user_count INTEGER
                    )
                ''')
                # Если таблица только что создана, добавляем начальное значение
                cursor.execute('INSERT OR IGNORE INTO user_counts (id, user_count) VALUES (?, ?)', (1, 0))
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")

        # Создаем таблицу new_bot_users
        try:
            with sqlite3.connect(db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS new_bot_users (
                        id INTEGER PRIMARY KEY,
                        chat_id INTEGER,
                        first_name TEXT,
                        username TEXT,
                        user_status INTEGER,
                        news_subscribe INTEGER,
                        last_uid_news INTEGER
                    )
                ''')
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")

    def examination_count_user(self)->bool:
        """Проверяет на 0 кол-во prymary_key в таблице bot_users"""
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_count FROM user_counts WHERE id = 1')
            result = cursor.fetchone()
            if 0 in result:
                return True
            else:
                return False
        pass
    
    def add_data(self, table_name, chat_id, first_name, username, user_status, news_subscribe, last_uid_news):
        """Транзакция для добавления данных пользователя и изменение счетчика"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                query = f'INSERT INTO {table_name} (chat_id, first_name, username, user_status, news_subscribe, last_uid_news) VALUES (?, ?, ?, ?, ?, ?)'
                data = (chat_id, first_name, username, user_status, news_subscribe, last_uid_news)

                cursor.execute(query, data)
                if table_name == 'bot_users':
                    cursor.execute('UPDATE user_counts SET user_count = user_count + 1 WHERE id = 1')
                    conn.commit()
                else:
                    conn.commit()
                print(f'Данные {chat_id} успешно добавлены')

        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе add_data: {e}")
    
    def loging_users(self, chat_id) -> bool:
        """Проверяет наличие пользователя в таблице bot_users"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM bot_users WHERE chat_id = ? LIMIT 1', (chat_id,))
                user_id = cursor.fetchone()
                if user_id is not None:
                    return True
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе loging_users: {e}")

        return False

    def admin_users(self, table, chat_id, status) -> bool:
        """Проверка статуса: Админ"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f'SELECT id FROM {table} WHERE chat_id = ? AND user_status = ? LIMIT 1', (chat_id, status))
                user_id = cursor.fetchone()

                if user_id is not None:
                    return True

        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе admin_users: {e}")

        return False

    def users_list(self, table:str) -> dict:
        """Возвращает словарь ключ: first_name, значение: chat_id"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f'SELECT first_name, chat_id FROM {table}')
                user_data = cursor.fetchall()
                user_dict = {first_name: chat_id for first_name, chat_id in user_data}
                print(user_dict)
                return user_dict
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе users_list: {e}")
            return {}
        
    def user_chat_id(self, table: str) -> list:
        """Получает список chat_id пользователей"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f'SELECT chat_id FROM {table};')
                chat_ids = [str(row[0]) for row in cursor.fetchall()]
                return chat_ids
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе user_chat_id: {e}")
            return []
        
    def print_info_user(self, table:str, chat_id:str) -> str:
        """Возвращает информацию о пользователе"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f'SELECT * FROM {table} WHERE chat_id = ?', (chat_id,))
                user_data = cursor.fetchone()
                if table == 'bot_users':
                    if user_data:
                        user_info = f'Это пользователь с именем {user_data[2]} и ником @{user_data[3]}.\n'
                        user_info += f'Является {"Юзером" if user_data[4] == 0 else "Суперюзером" }.\n'
                        user_info += f'{"Не подписан" if user_data[5] == 0 else "Подписан" } на новости.'
                        user_info += 'Сделать....'
                        return user_info
                    else:
                        return "Пользователь не найден в базе данных."
                elif table == 'new_bot_users':
                    if user_data:
                        user_info = f'Это пользователь с именем {user_data[2]} и ником @{user_data[3]}. \nРазрешить доступ к функционалу?'
                        return user_info
                    pass
                else:
                    print ('В методе print_info_user в ветке выбора таблиц произошла ошибка')

        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе print_info_user: {e}")
            return "Произошла ошибка при работе с базой данных."
    
    def change_db(self, table:str, chat_id:str, column:str, data) -> bool:
        """Обновляет данные в указанной таблице и колонке для определенного чата."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                query = f'UPDATE {table} SET {column} = ? WHERE chat_id = ?'
                cursor.execute(query, (data, chat_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе change_db: {e}")
            return False
        pass

    def dellete_users(self, table:str, chat_id:str) -> bool:
        """Удаляет данные пользователя в таблице по chat_id, меняет счетчик"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f'DELETE FROM {table} WHERE chat_id = ?', (chat_id,))
                if table == 'bot_users':
                    cursor.execute('UPDATE user_counts SET user_count = user_count - 1 WHERE id = 1')
                    conn.commit()
                    return True
                else:
                    conn.commit()
                    return True
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе delete_user: {e}")
            return False
        pass

    def postpone_users(self, table_a:str, table_b:str, chat_id:str) -> bool:
        """Переносить данные пользователя из таблицы new_bot_users в таблицу bot_users"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f'SELECT chat_id, first_name, username, user_status, news_subscribe, last_uid_news FROM {table_a} WHERE chat_id = ?', (chat_id,))
                user_data = cursor.fetchone()
                if user_data:
                    self.add_data(table_b, *user_data)
                    cursor.execute(f'DELETE FROM {table_a} WHERE chat_id = ?', (chat_id,))
                    conn.commit()
                    return True
                else:
                    return False
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе postpone_user: {e}")
            return False

    def change_users(self, table:str, chat_id:str, comand:str) -> str:
        """Обращается к БД, обращется к таблице, находит пользователя по id менет данные в столбце или удяляет запись"""
        check = 'Изменения внесены!'
        no_check = 'Изменения не внесены, обратитесь к администратору!'

        # Делает пользователя обычным пользователем
        if comand =='do_user':
            req = self.change_db(table, chat_id, 'user_status', 0)
            return check if req == True else no_check
 
        #Делает пользователя админом
        elif comand =='new_admin':
            req = self.change_db(table, chat_id, 'user_status', 1)
            return check if req == True else no_check
        
        # Удаляет пользователя из БД
        elif comand == 'dellete_user':
            req = self.dellete_users(table, chat_id)
            return check if req == True else no_check

        # Переносит пользователя из new_bot_users в bot_users
        elif comand == 'yes_new_users':
            req = self.postpone_users(table, 'bot_users', chat_id)
            return check if req == True else no_check
        
        # На случай если что-то сломается
        else:
            return 'Произошла ошибка, обратитесь к администратору.'
            print('В методе change_users произошла ошибка')
        pass

    #Списки чат-айди для управления рассылками
    def chat_id_list(self, table:str, column:str, value:int) -> list:
        """Собирает список chat_id по данным столбца"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f'SELECT chat_id FROM {table} WHERE {column} = ?', (value,))
                chat_ids = [row[0] for row in cursor.fetchall()]
                return chat_ids
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных в методе chat_id_list: {e}")
            return []
        pass

    #

        
    




class Valute:
    def __init__(self):
        pass

    def pars_valute(self):
        # URL API Центрального банка России для получения курса валют
        url = "https://www.cbr-xml-daily.ru/daily_json.js"

        try:
            response = requests.get(url)
            data = response.json()
            
            # Печатаем информацию о валютах
            for currency_code, currency_info in data['Valute'].items():
                print(f"Код валюты: {currency_code}")
                print(f"Название: {currency_info['Name']}")
                print(f"Курс к рублю: {currency_info['Value']} рублей")
                print(f"Номинал: {currency_info['Nominal']}")
                print("------------")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
        except ValueError as e:
            print(f"Ошибка при обработке JSON-данных: {e}")








        

    


audio = Audio_file(folder_a, folder_b)
valute = Valute()
db = DataBase(db_name)

#audio.print_available_dates(audio.available_dates(folder_b))
#audio.copy_file(folder_a, folder_b) #Сценарий автообновления папки бота
#audio.dellete_audio_folders(folder_b) #Сценарий автоудаления папки бота
#db.create_db_users() # Сценарий создания таблицы пользователей
print(db.users_list('bot_users'))
print(db.user_chat_id('bot_users'))
print(db.chat_id_list('bot_users', 'user_status', 1))


#valute.pars_valute()

"""cursor.execute('SELECT id FROM avtoradio_bot_users WHERE id=? AND user_status=1', (user_id,))
return bool(cursor.fetchall())"""
        
        

        
# Модули
from config import folder_a, folder_b
from users_rqests_map import mounth

# Библиотеки
from os import listdir, path
from shutil import copytree
from datetime import datetime
from re import match
import shutil

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


        

        

    


audio = Audio_file(folder_a, folder_b)

audio.print_available_dates(audio.available_dates(folder_b))
#audio.copy_file(folder_a, folder_b) #Сценарий автообновления папки бота
#audio.dellete_audio_folders(folder_b) #Сценарий автоудаления папки бота

        
        

        
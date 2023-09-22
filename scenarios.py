import schedule
from clases import audio
from config import folder_a, folder_b

async def auto_update_folders():
    audio.copy_file(folder_a, folder_b)

async def auto_delete_folders():
    audio.dellete_audio_folders(folder_b) 

def schedule_auto_update():
    # Автообновление папок и файлов в них
    schedule.every().hour.at(":07").do(auto_update_folders)
    schedule.every().hour.at(":37").do(auto_update_folders)
    
    # Автоудаление папок
    schedule.every().day.at("23:50:00").do(auto_delete_folders)

async def main_work():
    schedule_auto_update()
    pass

    


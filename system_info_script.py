import platform
import os
import psutil
import getpass
import datetime

def get_system_info():
    system_info = {}

    # Получаем информацию о процессоре
    system_info['Процессор'] = platform.processor()

    # Получаем информацию о видеокарте (этот способ может быть не всегда точным, зависит от платформы)
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            system_info['Видеокарта'] = gpus[0].name
        else:
            system_info['Видеокарта'] = 'Информация о видеокарте недоступна'
    except ImportError:
        system_info['Видеокарта'] = 'Не установлен модуль GPUtil'

    # Получаем информацию об ОЗУ
    system_info['ОЗУ'] = f"{round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} ГБ"

    # Получаем информацию о свободном месте на дисках
    drives_info = psutil.disk_partitions()
    for drive in drives_info:
        drive_name = drive.device
        drive_space = psutil.disk_usage(drive_name)
        system_info[f'Свободное место на диске {drive_name}'] = f"{round(drive_space.free / (1024.0 ** 3), 2)} ГБ"

    # Получаем имя пользователя
    system_info['Имя пользователя'] = getpass.getuser()

    return system_info

def save_to_text_file(file_path, data, signature):
    with open(file_path, 'w') as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")
        file.write(f"\nПодпись: {signature}\n")

if __name__ == "__main__":
    system_info = get_system_info()

    # Задайте путь к папке, куда нужно сохранить файл
    folder_path = "D:\Eugene"
    # Задайте имя файла
    file_name = "system_info.txt"

    file_path = os.path.join(folder_path, file_name)

    # Получаем текущую дату и время
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Подпись - имя пользователя и дата
    signature = f"Пользователь: {system_info['Имя пользователя']}, Дата: {current_date}"

    save_to_text_file(file_path, system_info, signature)
    print(f"Информация о системе сохранена в файле {file_name} в папке {folder_path}")

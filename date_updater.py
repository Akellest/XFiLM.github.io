import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

directory_path = os.path.join('html')

latest_file = None
latest_time = 0

# Получаем список всех HTML файлов в указанной директории
html_files = [f for f in os.listdir(directory_path) if f.endswith('.html')]
print(f"Найдено HTML файлов: {len(html_files)}")
print(html_files)

# Находим последний измененный файл
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    
    if os.path.isfile(file_path):
        file_mtime = os.path.getmtime(file_path)
        
        if file_mtime > latest_time:
            latest_time = file_mtime
            latest_file = file_path

if latest_file:
    last_modified_date = datetime.fromtimestamp(latest_time).strftime('%d.%m.%Y')
    print(f'Последний измененный файл: {latest_file}')
    print(f'Дата последнего изменения: {last_modified_date}')

    html_file_path = os.path.join(directory_path, 'prescriptum.html')

    # Читаем содержимое оригинального файла в режиме r+
    with open(html_file_path, 'r+', encoding='utf-8') as html_file:
        content = html_file.read()
        
        # Используем регулярное выражение для замены только второй даты
        updated_content = re.sub(r'(\d{2}\.\d{2}\.\d{4})\s*—\s*(\d{2}\.\d{2}\.\d{4})', r'\1 — ' + last_modified_date, content)
        
        # Перемещаем указатель в начало файла и записываем обновленный контент
        html_file.seek(0)  # Перемещение указателя в начало
        html_file.write(updated_content)  # Запись обновленного контента
        html_file.truncate()  # Обрезка файла, если новый контент короче
            
else:
    print('Нет файлов в директории.')

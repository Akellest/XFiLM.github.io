import os
import re
from datetime import datetime

directory_path = os.path.join('html')

latest_file = None
latest_time = 0

html_files = [f for f in os.listdir(directory_path) if f.endswith('.html')]
print(f"Найдено HTML файлов: {len(html_files)}")
print(html_files)


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
    
    with open('html/prescriptum.html', 'r+', encoding='utf-8') as html_file:
        content = html_file.read()
        
        updated_content = re.sub(r'(\d{2}\.\d{2}\.\d{4})\s*—\s*(\d{2}\.\d{2}\.\d{4})', r'\1 — ' + last_modified_date, content)
        
        html_file.seek(0)
        html_file.write(updated_content)
        html_file.truncate()
else:
    print('Нет файлов в директории.')

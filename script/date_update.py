import os
import re
from datetime import datetime

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

    try:
        # Открываем файл prescriptum.html для редактирования
        prescriptum_file_path = os.path.join('html', 'prescriptum.html')
        print(f"Открываем файл: {prescriptum_file_path}")  # Проверка пути

        with open(prescriptum_file_path, 'r+', encoding='utf-8') as html_file:
            content = html_file.read()
            
            # Заменяем дату в контенте
            updated_content = re.sub(r'(\d{2}\.\d{2}\.\d{4})\s*—\s*(\d{2}\.\d{2}\.\d{4})', r'\1 — ' + last_modified_date, content)

            # Проверяем, были ли изменения
            if updated_content != content:
                print(f"content: {content}")
                print(f"updated_content: {updated_content}")

                # Перезаписываем файл
                html_file.seek(0)  # Перемещаем указатель в начало файла
                html_file.write(updated_content)  # Записываем обновленный контент
                html_file.truncate()  # Обрезаем файл, если обновленный контент короче
            else:
                print("Нет изменений в контенте.")
    except Exception as e:
        print(f"Произошла ошибка при записи в файл: {e}")
else:
    print('Нет файлов в директории.')

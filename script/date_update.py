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

    html_file_path = os.path.join(directory_path, 'prescriptum.html')

    # Читаем содержимое оригинального файла
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        # Заменяем дату в контенте
        updated_content = re.sub(r'(\d{2}\.\d{2}\.\d{4})\s*—\s*(\d{2}\.\d{2}\.\d{4})', r'\1 — ' + last_modified_date, content)

        print(f"content: {content}")
        print(f"updated_content: {updated_content}")

    # Удаляем оригинальный файл
    os.remove(html_file_path)
    print(f"Удален файл: {html_file_path}")

    # Создаем новый файл с обновленным контентом
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)  # Записываем обновленный контент

    # Проверяем содержимое нового файла
    with open(html_file_path, 'r', encoding='utf-8') as file:
        final_content = file.read()
        print("Содержимое файла после изменений:")
        print(final_content)
else:
    print('Нет файлов в директории.')

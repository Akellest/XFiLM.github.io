import os
import re
from bs4 import BeautifulSoup

def sort_table_by_first_column(soup):
    table = soup.find('table')
    rows = table.find_all('tr')
    headers = rows.pop(0)  # Сохраняем заголовки таблицы

    def sort_key(row):
        first_column = row.find('td', class_='first-column')
        if first_column is None:
            return (float('inf'), '')  # Переместить такие строки в конец
        first_column_text = first_column.text.strip()
        # Логика сортировки остается прежней
        if re.match(r'^\d+', first_column_text):
            return (0, first_column_text)
        elif re.match(r'^[а-яА-Я]', first_column_text):
            return (1, first_column_text.lower())
        elif re.match(r'^[a-zA-Z]', first_column_text):
            return (2, first_column_text.lower())
        else:
            return (3, first_column_text)

    sorted_rows = sorted(rows, key=sort_key)

    # Создаем новую таблицу и добавляем заголовок
    new_table = BeautifulSoup("<table></table>", 'html.parser').table
    new_table.append(headers)  # Добавляем заголовки в новую таблицу

    for row in sorted_rows:
        new_table.append(row)  # Добавляем отсортированные строки

    table.replace_with(new_table)


def update_html_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    sort_table_by_first_column(soup)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    
    print(f"Таблица отсортирована в файле '{filename}'.")

html_files = [f for f in os.listdir('html') if f.endswith('.html') and f.startswith('table')]
print(f"Найдено HTML файлов: {len(html_files)}")
print(html_files)

directory_path = os.path.join('html')

if not html_files:
    print("Не найдено HTML файлов для обработки.")
else:
    for html_file_path in html_files:
        html_file = os.path.join(directory_path, html_file_path)
        update_html_file(html_file)
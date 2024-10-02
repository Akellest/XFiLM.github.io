import os
import re
from bs4 import BeautifulSoup

def sort_table_by_first_column(soup):
    table = soup.find('table')
    rows = table.find_all('tr')

    def sort_key(row):
        # Получаем текст из первой колонки
        first_column_text = row.find('td', class_='first-column').text.strip()

        # Определяем сортировочный ключ
        if re.match(r'^\d+', first_column_text):
            return (0, first_column_text)  # Цифры идут первыми
        elif re.match(r'^[а-яА-Я]', first_column_text):
            return (1, first_column_text.lower())  # Русские буквы идут вторыми
        elif re.match(r'^[a-zA-Z]', first_column_text):
            return (2, first_column_text.lower())  # Английские буквы идут третьими
        else:
            return (3, first_column_text)  # Остальные символы в конце

    sorted_rows = sorted(rows, key=sort_key)

    # Создаем новую таблицу
    new_table = BeautifulSoup("<table></table>", 'html.parser').table

    for row in sorted_rows:
        new_table.append(row)

    # Заменяем старую таблицу на новую
    table.replace_with(new_table)

def update_html_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    sort_table_by_first_column(soup)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Таблица отсортирована в файле '{filename}'.")

# Поиск всех HTML файлов с именем table*.html
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f.startswith('table')]
print(f"Найдено HTML файлов: {len(html_files)}")
print(html_files)

if not html_files:
    print("Не найдено HTML файлов для обработки.")
else:
    for html_file in html_files:
        update_html_file(html_file)
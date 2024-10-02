import os
import re
from bs4 import BeautifulSoup
import logging

# Настройка логирования
logging.basicConfig(filename='update_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sort_table_by_first_column(soup):
    table = soup.find('table')
    rows = table.find_all('tr')

    def sort_key(row):
        first_column_text = row.find('td', class_='first-column').text.strip()
        if re.match(r'^\d+', first_column_text):
            return (0, first_column_text)
        elif re.match(r'^[а-яА-Я]', first_column_text):
            return (1, first_column_text.lower())
        elif re.match(r'^[a-zA-Z]', first_column_text):
            return (2, first_column_text.lower())
        else:
            return (3, first_column_text)

    sorted_rows = sorted(rows, key=sort_key)
    new_table = BeautifulSoup("<table></table>", 'html.parser').table

    for row in sorted_rows:
        new_table.append(row)

    table.replace_with(new_table)

def update_html_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        sort_table_by_first_column(soup)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        logging.info(f"Таблица отсортирована в файле '{filename}'.")
    except Exception as e:
        logging.error(f"Ошибка при обработке файла '{filename}': {e}")

# Поиск всех HTML файлов
html_directory = '../html'
html_files = [f for f in os.listdir(html_directory) if f.endswith('.html') and f.startswith('table')]
logging.info(f"Найдено HTML файлов: {len(html_files)}: {html_files}")

if not html_files:
    logging.warning("Не найдено HTML файлов для обработки.")
else:
    for html_file in html_files:
        update_html_file(os.path.join(html_directory, html_file))

logging.info("Скрипт завершил выполнение.")

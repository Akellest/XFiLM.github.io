import os
import re
import string
from bs4 import BeautifulSoup

# Определяем порядок символов
digits = "0123456789"
letters = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz" \
          "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"

# Все печатные ASCII символы
all_ascii = string.printable

# Остальные символы, которых нет в digits и letters
middle_chars = ''.join(ch for ch in all_ascii if ch not in digits and ch not in letters)

CUSTOM_ORDER = digits + middle_chars + letters
order_map = {ch: i for i, ch in enumerate(CUSTOM_ORDER)}

def sort_table_by_first_column(soup):
    table = soup.find('table')
    rows = table.find_all('tr')
    headers = rows.pop(0)  # Заголовки

    def sort_key(row):
        first_column = row.find('td', class_='first-column')
        if first_column is None:
            return (float('inf'), '')
        text = first_column.text.strip()
        if not text:
            return (float('inf'), '')
        first_char = text[0]
        priority = order_map.get(first_char, len(order_map))
        return (priority, text.lower())

    sorted_rows = sorted(rows, key=sort_key)

    new_table = BeautifulSoup("<table></table>", 'html.parser').table
    new_table.append(headers)
    for row in sorted_rows:
        new_table.append(row)
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

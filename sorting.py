import os
import string
from bs4 import BeautifulSoup

digits = " 0123456789"
letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz"

all_ascii = string.printable
middle_chars = ''.join(ch for ch in all_ascii if ch not in digits and ch not in letters and ch != ' ')

CUSTOM_ORDER = digits + middle_chars + letters
order_map = {ch: i for i, ch in enumerate(CUSTOM_ORDER)}

def char_key(ch):
    # Возвращаем индекс символа в order_map или очень большое число, если символ неизвестен
    return order_map.get(ch, len(order_map) + ord(ch))

def sort_key(row):
    first_col = next((td for td in row.find_all('td') if 'first-column' in td.get('class', [])), None)
    if first_col is None:
        return [float('inf')]
    link = first_col.find('a')
    if link:
        text = link.text.strip().lower()
    else:
        text = first_col.text.strip().lower()
    if not text:
        return [float('inf')]
    key = [char_key(ch) for ch in text]
    print(f"Сортировочный ключ для '{text}': {key}")
    return key


def sort_table_by_first_column(soup):
    table = soup.find('table')
    if table is None:
        print("Таблица не найдена в файле.")
        return

    rows = table.find_all('tr')
    if not rows:
        return

    # Проверяем, есть ли заголовок (строка с <th>)
    first_row = rows[0]
    if first_row.find('th'):
        headers = rows.pop(0)
    else:
        headers = None  # Заголовка нет

    sorted_rows = sorted(rows, key=sort_key)

    new_table = BeautifulSoup("<table></table>", 'html.parser').table
    if headers:
        new_table.append(headers)
    for row in sorted_rows:
        new_table.append(row)
    table.replace_with(new_table)


def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    sort_table_by_first_column(soup)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"Таблица отсортирована в '{filepath}'")
import os
import string
from bs4 import BeautifulSoup

# порядок: пробел + цифры
digits = " 0123456789"
# только строчные буквы в правильном порядке (рус. + англ.)
letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz"

all_ascii = string.printable
# все остальные печатные символы, кроме пробела, цифр и букв
middle_chars = ''.join(
    ch for ch in all_ascii
    if ch not in digits and ch not in letters and ch != ' '
)

CUSTOM_ORDER = digits + middle_chars + letters
order_map = {ch: i for i, ch in enumerate(CUSTOM_ORDER)}

def char_key(ch):
    return order_map.get(ch, len(order_map) + ord(ch))

def sort_key(row):
    # находим <td> с классом first-column (даже если несколько классов)
    first_col = next(
        (td for td in row.find_all('td') if 'first-column' in td.get('class', [])),
        None
    )
    if first_col is None:
        return [float('inf')]
    # вытаскиваем текст из <a> или из ячейки
    link = first_col.find('a')
    text = (link.text if link else first_col.text).strip().lower()
    if not text:
        return [float('inf')]
    key = [char_key(ch) for ch in text]
    print(f"Сортировочный ключ для '{text}': {key}")
    return key

def sort_table_by_first_column(soup):
    table = soup.find('table')
    if not table:
        print("Таблица не найдена.")
        return

    rows = table.find_all('tr')
    if not rows:
        return

    # если в первой строке есть <th>, считаем её заголовком
    first_row = rows[0]
    if first_row.find('th'):
        headers = rows.pop(0)
    else:
        headers = None

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

    print(f"Отсортировано: {filepath}")

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
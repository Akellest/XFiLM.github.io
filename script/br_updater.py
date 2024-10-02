import os
import numpy as np  # Необходим для работы с nan
from bs4 import BeautifulSoup

def update_html_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Обработка ссылок
    for link in soup.find_all('a'):
        link_text = link.text
        parts = link_text.split('/Slash/')
        new_content = BeautifulSoup("", 'html.parser')

        for i, part in enumerate(parts):
            new_link = soup.new_tag('a', href=link['href'])
            new_link.string = part.strip()
            new_content.append(new_link)

            if i < len(parts) - 1:
                new_content.append(soup.new_tag('br'))  # Используем <br> для переноса
                new_content.append('/')  # Добавляем символ "/"
                new_content.append(soup.new_tag('br'))  # Перенос строки после "/"

        link.replace_with(new_content)

    # Удаление значений None и nan из второго и пятого столбца
    for tr in soup.find_all('tr'):  # Ищем все строки таблицы
        # Удаляем значения в 2-ом столбце
        second_column = tr.find_all('td')[1] if len(tr.find_all('td')) > 1 else None
        if second_column:
            if second_column.text.strip() in ["None", "nan"]:  # Проверка на "None" или "nan"
                second_column.clear()  # Удаляем содержимое ячейки

        # Удаляем значения в 5-ом столбце
        fifth_column = tr.find_all('td')[4] if len(tr.find_all('td')) > 4 else None
        if fifth_column:
            if fifth_column.text.strip() in ["None", "nan"]:  # Проверка на "None" или "nan"
                fifth_column.clear()  # Удаляем содержимое ячейки

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Замена завершена в '{filename}'.")

# Поиск всех HTML файлов, кроме index.html и других исключаемых файлов
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html' and f != 'table-header.html' and f != '404.html']
print(f"Найдено HTML файлов: {len(html_files)}")
print(html_files)  # Вывод списка файлов в консоль

if not html_files:
    print("Не найдено HTML файлов для обработки.")
else:
    for html_file in html_files:
        update_html_file(html_file)
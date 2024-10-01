import os
from bs4 import BeautifulSoup

# Функция для обновления ссылок в HTML-файле
def update_html_file(filename):
    # Чтение исходного HTML-файла
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Парсинг HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Поиск всех ссылок в документе
    for link in soup.find_all('a'):
        # Получаем текст внутри ссылки
        link_text = link.text  # Только текст ссылки

        # Разделяем текст по символу '/'
        parts = link_text.split('/')

        # Создаем новый контент с переносами строк
        new_content = BeautifulSoup("", 'html.parser')

        for i, part in enumerate(parts):
            # Добавляем текст ссылки
            new_link = soup.new_tag('a', href=link['href'])  # Создаем новый <a> элемент
            new_link.string = part.strip()  # Добавляем часть текста

            # Вставляем ссылку в новый контент
            new_content.append(new_link)

            # Если это не последняя часть, добавляем символ '/'
            if i < len(parts) - 1:
                new_content.append(soup.new_tag('br'))  # Перенос строки перед "/"
                new_content.append('/')  # Сам символ "/"
                new_content.append(soup.new_tag('br'))  # Перенос строки после "/"

        # Заменяем содержимое ссылки на новый контент
        link.replace_with(new_content)

    # Сохранение изменений в исходный HTML файл
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Замена завершена, изменения сохранены в '{filename}'.")

# Получаем список всех HTML файлов в корневой папке, кроме index.html
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']

# Обрабатываем каждый HTML файл
for html_file in html_files:
    update_html_file(html_file)

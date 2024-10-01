from bs4 import BeautifulSoup

# Чтение исходного HTML-файла
with open('updated_example.html', 'r', encoding='utf-8') as file:
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

# Сохранение изменений в новый HTML файл
with open('updated_example.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("Замена завершена, изменения сохранены в 'updated_example.html'.")

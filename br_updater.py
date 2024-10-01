import os
from bs4 import BeautifulSoup

def update_html_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    for link in soup.find_all('a'):
        link_text = link.text
        parts = link_text.split('/')
        new_content = BeautifulSoup("", 'html.parser')

        for i, part in enumerate(parts):
            new_link = soup.new_tag('a', href=link['href'])
            new_link.string = part.strip()
            new_content.append(new_link)

            if i < len(parts) - 1:
                new_content.append(soup.new_tag('br'))
                new_content.append('/')
                new_content.append(soup.new_tag('br'))

        link.replace_with(new_content)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Замена завершена в '{filename}'.")

# Поиск всех HTML файлов, кроме index.html
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']
print(f"Найдено HTML файлов: {len(html_files)}")
print(html_files)  # Вывод списка файлов в консоль

if not html_files:
    print("Не найдено HTML файлов для обработки.")
else:
    for html_file in html_files:
        update_html_file(html_file)

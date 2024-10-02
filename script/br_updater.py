import os
import numpy as np
from bs4 import BeautifulSoup

def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    for link in soup.find_all('a'):
        link_text = link.text
        parts = link_text.split('/Slash/')
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

    for tr in soup.find_all('tr'):
        second_column = tr.find_all('td')[1] if len(tr.find_all('td')) > 1 else None
        if second_column:
            if second_column.text.strip() in ["None", "nan"]:
                second_column.clear()

        fifth_column = tr.find_all('td')[4] if len(tr.find_all('td')) > 4 else None
        if fifth_column:
            if fifth_column.text.strip() in ["None", "nan"]:
                fifth_column.clear()

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Замена завершена в '{filepath}'.")

print(os.listdir())
os.listdir(os.getcwd())

html_directory = os.path.join('..', 'html')
print(html_directory)
os.listdir(html_directory)


html_files = [os.path.join(html_directory, f) for f in os.listdir(html_directory) 
              if f.endswith('.html') and f not in ['index.html', 'table-header.html', '404.html']]

print(f"Найдено HTML файлов: {len(html_files)}")
print(html_files)

if not html_files:
    print("Не найдено HTML файлов для обработки.")
else:
    for html_file in html_files:
        update_html_file(html_file)
input()
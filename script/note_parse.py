import re
from imdb import Cinemagoer
from openpyxl import Workbook
from googlesearch import search
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm


def get_imdb_info(ia, movie_id):
    the_matrix = ia.get_movie(movie_id)

    if the_matrix['title'] != the_matrix['original title']:
        foreign_title = f"{the_matrix['title']} /Slash/ {the_matrix['original title']}"
    else:
        foreign_title = the_matrix['title']

    if the_matrix.get('series years', 'N/A') != "N/A":
        year = the_matrix.get('series years', 'N/A')
    else:
        year = the_matrix.get('year', 'N/A')

    note_list = [
        the_matrix.get('localized title', 'N/A'),
        the_matrix.get('full-size cover url', 'N/A'),
        foreign_title,
        year
    ]

    return note_list


def find_movie_id(ia, query):
    search_results = ia.search_movie(query)

    if search_results:
        first_result = search_results[0]
        movie_id = first_result.movieID
        return movie_id
    else:
        return None


def findLinkViaGoogle(title):
    query = f"{title} imdb"
    try:
        for url in search(query, num_results=5):
            if 'imdb.com/title/tt' in url:
                url = url.replace('m.imdb.com', 'www.imdb.com')
                clean_url = re.match(r'(https://www\.imdb\.com/title/tt\d+/)', url)
                if clean_url:
                    return clean_url.group(1)
        print(f"ERROR: No valid IMDb link found for title: '{title}'")
        return None
    except Exception as e:
        print(f"ERROR WHILE SEARCHING IMDB LINK FOR '{title}': {e}")
        return None


def movieToExcel(title):
    ia = Cinemagoer('https', languages='ru-RU')  # Создаем экземпляр для каждого процесса
    movie_id = find_movie_id(ia, title)

    if movie_id is not None:
        movie_info = get_imdb_info(ia, movie_id)
        return movie_info, f"https://www.imdb.com/title/tt{movie_id}/", None
    else:
        movieLinkViaGoogle = findLinkViaGoogle(title)
        # Если после повторной попытки фильм найден, добавляем его в таблицу
        if movieLinkViaGoogle is not None:
            movie_id = re.search(r'tt(\d+)', movieLinkViaGoogle).group(1)
            movie_info = get_imdb_info(ia, movie_id)
            return movie_info, f"https://www.imdb.com/title/tt{movie_id}/", None
        else:
            print(f"ERROR FOR FILM {title}")
            return None, None, title  # Возвращаем название фильма для обработки ошибок


def main():
    filename = 'films.txt'
    error_list = []  # Список для хранения названий фильмов с ошибками

    with open(filename, 'r', encoding='utf-8') as file:
        films = file.readlines()

    films_list = [film.strip() for film in films if film.strip()]  # Удаляем пустые строки

    # Используем ProcessPoolExecutor для параллельной обработки
    with ProcessPoolExecutor() as executor:
        # Используем tqdm для отображения прогресса
        results = list(tqdm(executor.map(movieToExcel, films_list), total=len(films_list), desc="Processing Movies"))

    wb2 = Workbook()
    ws2 = wb2.active

    for i, (movie_info, imdb_link, error_title) in enumerate(results, start=1):
        if error_title:
            error_list.append(error_title)
        elif movie_info:  # Проверяем, что movie_info не None перед записью
            add_movie_to_excel(ws2, movie_info, imdb_link, i)

    # Сохраняем Excel файл
    wb2.save('output.xlsx')

    non_empty_lines = len(films_list)
    total_excel_rows = len(results) - len(error_list)  # Учитываем количество ошибок

    print(f"Count films.txt: {non_empty_lines}")
    print(f"Total errors: {len(error_list)}")  # Выводим количество ошибок

    # Сохраняем ошибки в текстовый файл
    if error_list:
        with open('error_films.txt', 'w', encoding='utf-8') as error_file:
            for error in error_list:
                error_file.write(error + '\n')  # Записываем названия фильмов с новой строки


def add_movie_to_excel(ws2, movie_info, imdb_link, row_index):
    ws2.append(movie_info)
    ws2[f"A{row_index}"].hyperlink = imdb_link


if __name__ == '__main__':
    main()
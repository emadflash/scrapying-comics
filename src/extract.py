import logging
import requests
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from src.fetch import fetch_metadata_from_soup, fetch_urls_from_page

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

base_url = 'https://readcomiconline.to'
list_of_genres = [
    'Action',
    'Adventure',
    'Anthology',
    'Anthropomorphic',
    'Biography',
    'Children',
    'Comedy',
    'Crime',
    'Drama',
    'Family',
    'Fantasy',
    'Fighting',
    'Graphic Novels',
    'Historical',
    'Horror',
    'Leading Ladies',
    'LGBTQ',
    'Literature',
    'Manga',
    'Martial Arts',
    'Mature',
    'Military',
    'Movies & TV',
    'Music',
    'Mystery',
    'Mythology',
    'Personal',
    'Political',
    'Post-Apocalyptic',
    'Psychological',
    'Pulp',
    'Religious',
    'Robots',
    'Romance',
    'School Life',
    'Sci-Fi',
    'Slice of Life',
    'Sport',
    'Spy',
    'Superhero',
    'Supernatural',
    'Suspense',
    'Thriller',
    'Vampires',
    'Video Games',
    'War',
    'Western',
    'Zombies',
]


def create_genre_onehot_list(genre):
    onehot_list = [0] * len(list_of_genres)
    for i in genre:
        if i in list_of_genres:
            genre_index = list_of_genres.index(i)
            onehot_list[genre_index] = 1
    return onehot_list


def generate_csv_style(meta):
    santize = lambda x : x.replace(',','-')
    _add = lambda x : ',' + x
    _add_if = lambda x : _add(santize(x)) if x != None else _add('None')

    csv_string = ''
    csv_string += meta['title']
    csv_string += _add(meta['status'])
    csv_string += _add(meta['views'])
    csv_string += _add(meta['publisher'])
    csv_string += _add_if(meta['publication_date'].get('from'))
    csv_string += _add_if(meta['publication_date'].get('to'))
    for i in create_genre_onehot_list(meta['genre']):
        csv_string += _add(str(i))
    return csv_string


def url_handler(url, file_csv):
    req = requests.get(url)
    print(f'[*] extracting metadata from {url}')
    soup = BeautifulSoup(req.text, 'html.parser')
    try:
        meta = fetch_metadata_from_soup(soup=soup)
    except Exception as exception:
        logging.info(f"[failed_to_parse] {url}")
    else:
        with open(file_csv, 'a') as f:
            f.write(generate_csv_style(meta) + '\n')


def write_urls(url_file, base_list_url, end_page) -> list:
    curr_page = 1
    urls = []
    while curr_page <= end_page:
        payload = {
            'page': curr_page
        }
        source = requests.get(base_list_url, params=payload)
        if source.ok:
            print("[*] fetching urls; ", source.url)
            soup = BeautifulSoup(source.text, 'html.parser')
            for i in fetch_urls_from_page(soup=soup):
                with open(url_file, 'a') as f:
                    if i not in urls:
                        f.write(i + '\n')
                        urls.append(i)
                    else:
                        continue
        else:
            print("[*] error: unable to fetch urls from ", source.url)
        curr_page += 1


def write_metadata(url_file, file_csv, start_url_index, end_url_index):
    with open(url_file, 'r') as f:
        unfiltered_urls = f.readlines()
        urls = list(map(lambda x: x.strip('\n'), unfiltered_urls))
        threads = []
        # TODO executor.map(url_handler,urls)
        for url_index, url in enumerate(urls[start_url_index: end_url_index]):
            try:
                url = urljoin(base_url, url)
                thread = threading.Thread(target=url_handler, args=[url, file_csv])
                threads.append(thread)
            except:
                print(f'[*] error: fetching metadata from url {url}; url_handler called')
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


def generate_csv_one_go(file_csv, base_list_url, start_page, end_page):
    curr_page = start_page
    urls = []
    threads = []
    while curr_page <= end_page:
        payload = {
            'page': curr_page
        }
        source = requests.get(base_list_url, params=payload)
        if source.ok:
            print("[*] fetching urls; ", source.url)
            soup = BeautifulSoup(source.text, 'html.parser')
            for url in fetch_urls_from_page(soup=soup):
                if url not in urls:
                    url = urljoin(base_list_url, url)
                    thread = threading.Thread(target=url_handler, args=[url, file_csv])
                    threads.append(thread)
                    urls.append(url)
                else:
                    continue

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            threads.clear()
        else:
            print("[*] error: unable to fetch urls from ", source.url)
            logging.info("[failed_to_extract_url]", source.url)
        curr_page += 1

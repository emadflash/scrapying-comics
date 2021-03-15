from fetch import fetch_metadata_from_soup, fetch_all_urls
import requests
from bs4 import BeautifulSoup
import threading
from urllib.parse import urljoin

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
    print(f'[*] fetching meta data from {base_url + url}')
    soup = BeautifulSoup(req.text, 'html.parser')
    meta = fetch_metadata_from_soup(soup=soup)
    with open(file_csv, 'a') as f:
        f.write(generate_csv_style(meta) + '\n')


def write_urls_to_file(url_file, total_page_count):
    urls = fetch_all_urls(total_page_count)
    with open(url_file,'w') as f:
        print(f'[$] Writing urls to {url_file}.....')
        for i in urls: 
            f.write(i + '\n')
    print(f'[*] success: wrote {len(urls)} to {url_file}')


def write_metadata_to_file(url_file, file_csv, from_index, to_index):
    with open(url_file, 'r') as f:
        unfiltered_urls = f.readlines()
        urls = list(map(lambda x: x.strip('\n'), unfiltered_urls))
        threads = []
        # TODO executor.map(url_handler,urls)
        for url_index, url in enumerate(urls[from_index: to_index]):
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

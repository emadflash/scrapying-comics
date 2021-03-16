import re
import requests
from bs4 import BeautifulSoup


def fetch_urls_from_page(soup) -> list:
    tr = soup.findAll('div', {'class': 'col cover'})
    for i in tr:
        a = i.find('a')
        href = a['href']
        yield href


def get_start_end_date(publication_date) -> tuple[str, str]:
    if publication_date.find('-') > 0:
        start, end = publication_date.split(' - ')
    else:
        start = publication_date
        end = None
    return (start, end)


def fetch_metadata_from_soup(soup) -> dict:
    barContent = soup.find('div', class_='col info')
    genre = []
    p = barContent.findAll('p')
    p_genre = p[0]
    for i in p_genre.findAll('a'):
        genre.append(i.text)

    a_tag_text = lambda x : p[x].find('a').text
    clean_col = lambda x : x.strip('\n \r').partition(':\xa0')[2]
    remove_comma = lambda x : re.sub('[^\d\.]', '', x)
    sanitize = lambda x : x.replace(',',' ')
    start, end = get_start_end_date(clean_col(p[4].text))

    return {
            'title': sanitize(soup.find('h3').text),
            'genre': genre,
            'publisher': sanitize(a_tag_text(1)),
            'writer': sanitize(a_tag_text(2)),
            'artist': sanitize(a_tag_text(3)),
            'status': clean_col(p[5].text),
            'views': remove_comma(clean_col(p[6].text)),
            'publication_date': {
                    'from': start,
                    'to': end
                    }
            }

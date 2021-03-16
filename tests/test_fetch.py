import sys
sys.path.append('../src/')

import requests
from bs4 import BeautifulSoup
from fetch import fetch_metadata_from_soup, fetch_urls_from_page


comic_url = sys.argv[1]
r = requests.get(comic_url)
s = BeautifulSoup(r.text, 'html.parser')

try:
    # print(fetch_metadata_from_soup(s))
    print('[*] success: fetch_metadata_from_soup')
except:
    print('[*] failed: fetch_metadata_from_soup')

try:
    fetch_urls_from_page(1)
    print('[*] success: fetch_urls_from_page')
except:
    print('[*] failed: fetch_urls_from_page')

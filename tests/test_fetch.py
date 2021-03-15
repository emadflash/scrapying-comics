import sys
sys.path.append('../src/')

import requests
from bs4 import BeautifulSoup
from fetch import fetch_metadata_from_soup, fetch_all_urls


comic_url = sys.argv[1]
r = requests.get(comic_url)
s = BeautifulSoup(r.text, 'html.parser')

try:
    # print(fetch_metadata_from_soup(s))
    print('[*] success: fetch_metadata_from_soup')
except:
    print('[*] failed: fetch_metadata_from_soup')

try:
    fetch_all_urls(1)
    print('[*] success: fetch_all_urls')
except:
    print('[*] failed: fetch_all_urls')


#!/usr/bin/env python3
import sys
import time
import argparse
import logging
from src.extract import write_urls, generate_csv_one_go

max_page_count = 446
base_comic_list_url = "https://readcomiconline.to/ComicList"

default_url_file = "urls.txt"
default_csv_file = "dataset.csv"

sleep_request = 3       # minutes

parser = argparse.ArgumentParser(description="generate url/csv files of content from readcomiconline.to")

parser.add_argument('--extract-urls', action='store_true', help='generate file with all comic urls')
parser.add_argument('--one-go', action='store_true', help='extract metadata while extract urls')
parser.add_argument('--url-file',  type=str)
parser.add_argument('--csv-file',  type=str)

args = parser.parse_args()


def set_file(File, default_file):
    file_status = args.__dict__[File]
    if file_status is None:
        return default_file
    else:
        return file_status


url_file = set_file('url_file', default_url_file)
csv_file = set_file('csv_file', default_csv_file)


if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
else:
    if args.extract_urls:
        print(f"[*] extracting urls to {url_file}")
        try:
            write_urls(url_file, base_comic_list_url, max_page_count)
        except KeyboardInterrupt:
            print("[*] stopped fetching urls")
        except:
            print("[*] error: oops, something went wrong")
    elif args.one_go:
        try:
            generate_csv_one_go(csv_file, base_comic_list_url, 0, max_page_count)
        except:
            print("[*] error: oops, something went wrong")

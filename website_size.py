#
# Estimating the size of a website
# ________________________________
#
# example:
# python ./website_size.py --url https://hexdocs.pm/ratatouille/readme.html
#
# ref:
# https://practicaldatascience.co.uk/data-science/how-to-count-indexed-pages-using-python
#

import argparse
import requests
from requests_html import HTMLSession
from urllib.parse import urlparse, ParseResult


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(url):
    response = get_source("https://www.google.com/search?q=site%3A" + url)
    return response

def parse_results(response):
    string = response.html.find("#result-stats", first=True).text
    return int(string.split(' ')[1].replace(',',''))

def count_indexed_pages(url):
    response = get_results(url)
    return parse_results(response)

def append_http(url):
    p = urlparse(url, 'http')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''

    p = ParseResult('http', netloc, path, *p[3:])
    return p.geturl()

def main(url:str):
    # cleanup: append 'http://' if not exist
    url = append_http(url)
    # Extract domain from URL
    url = urlparse(url).netloc

    result = count_indexed_pages(url)
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Estimating the size of a website')
    parser.add_argument('--url', metavar='path', required=True, help='hackernews URL')
    args = parser.parse_args()

    main(args.url)

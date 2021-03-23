
import sys
from pagescrape import pagescrape
from mcqscrape import mcqscrape_html, write_to_html
from bs4 import BeautifulSoup
PAGE_URL = input("Enter the URL of the Page where you see links of all Subject related MCQs: ")  # noqa: E501


def main(url: str):
    if url == '':
        print("Please Enter a URL!")
        sys.exit()
    pages = pagescrape(url)
    mega_html = ''
    for k, v in pages.items():
        print("getting", k, "from ->", v, end=' ... ')
        mega_html += mcqscrape_html(v)
        print("Done!")
    write_to_html(BeautifulSoup(mega_html, 'html5lib').prettify(),
                  PAGE_URL.split('/')[-2])


main(PAGE_URL)

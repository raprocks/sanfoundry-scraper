import sys
from pagescrape import pagescrape
from bs4 import BeautifulSoup
from mcqscrape import mcqscrape_html, write_to_html
PAGE_URL = input("Enter the URL of the Page where you see links of all Subject related MCQs: ")  # noqa: E501


def main(url: str):
    if url == '':
        print("Please Enter a URL!")
        sys.exit()
    pages = pagescrape(url)
    mega_html = ''
    for PageTitle, PageUrl in pages.items():
        print("getting", PageTitle, "from ->", PageUrl, end=' ... ')
        mega_html += mcqscrape_html(PageUrl)
        print("Done!")
    write_to_html(BeautifulSoup(mega_html, 'lxml'),
                  PAGE_URL.split('/')[-2])


main(PAGE_URL)

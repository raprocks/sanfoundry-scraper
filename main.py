
from pagescrape import pagescrape
from mcqscrape import mcqscrape_html, write_to_html
from bs4 import BeautifulSoup
PAGE_URL = "https://www.sanfoundry.com/1000-object-oriented-programming-oops-questions-answers/"  # noqa: E501

pages = pagescrape(PAGE_URL)
mega_html = ''
with open('downloaded.json', 'w+') as fd:
    for k, v in pages.items():
        print("getting", k, "from ->", v, end=' ... ')
        mega_html += mcqscrape_html(v)
        print("Done!")
    write_to_html(BeautifulSoup(mega_html, 'lxml').prettify(),
                  PAGE_URL.split('/')[-2])

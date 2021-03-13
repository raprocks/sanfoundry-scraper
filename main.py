from pagescrape import pagescrape
from mcqscrape import mcqscrape_html

PAGE_URL = "https://www.sanfoundry.com/1000-object-oriented-programming-oops-questions-answers/"

pages = pagescrape(PAGE_URL)
down_data = {}
with open('downloaded.json', 'w+') as fd:
    for k, v in pages.items():
        print("getting", k, "from ->", v, end=' ... ')
        mcqscrape_html(v, PAGE_URL.split('/')[-2])
        print("Done!")

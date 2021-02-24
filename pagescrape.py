import requests
from bs4 import BeautifulSoup


def pagescrape(url: str):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    content = soup.find('div', class_='entry-content')
    tables = content.findAll('table')
    links = {}
    for table in tables:
        hrefs = {link.text.strip().replace(
            " ", '-'): link["href"] for link in table.findAll('a')}
        links.update(hrefs)
    return links


if __name__ == '__main__':
    results = pagescrape(
        "https://www.sanfoundry.com/1000-object-oriented-p\
            rogramming-oops-questions-answers/")
    print(results)

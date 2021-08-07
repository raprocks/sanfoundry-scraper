from typing import Dict
import requests
from bs4 import BeautifulSoup


def pagescrape(url: str) -> Dict[str, str]:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    content = soup.find('div', class_='entry-content')
    sf_contents = content.findAll('div', class_='sf-section')
    filtered_sf_content = [
        item for item in sf_contents
        if item.h2 is not None and item.table is not None
    ]
    tables = [item.table for item in filtered_sf_content]
    links = {}
    for table in tables:
        hrefs = {link.text.strip().replace(
            " ", '-'): link["href"] for link in table.findAll('a') if link.has_attr('href')}
        links.update(hrefs)
    return links

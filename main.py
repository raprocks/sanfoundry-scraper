import sys
import time
from argparse import ArgumentParser
from typing import List ,Optional
from concurrent.futures import ThreadPoolExecutor

from pagescrape import pagescrape
from mcqscrape import mcqscrape_html, write_to_html
from bs4 import BeautifulSoup

mul_threading: Optional[bool] = sys.argv[1:]

#added a little cli helper
parser = ArgumentParser(description="A CLI Tool for scrapping quizs from SANFOUNDARY" , usage="\n python main.py --thread --workers 15", epilog="Batmobile lost the wheel lol")
parser.add_argument("--url" , help="URL of quiz" , type=str , default=None , dest="url")
parser.add_argument("--thread" , action="store_true" , help="Uses Multithreading for scrapping")
parser.add_argument("--workers" , type=int , help="Maximum number of threads[ More number More speed but More Unstability]" , default=5)
args = parser.parse_args()

QUIZ_LIST: List[str] = []

def main(url: str):
    MEGA_HTML: str = ''
    if url == '':
        print("Please Enter a URL!")
        sys.exit()
    pages = pagescrape(url)
    for k, v in pages.items():
        print("getting", k, "from ->", v, end=' ... ')
        MEGA_HTML += mcqscrape_html(v)
        print("Done!")

    write_to_html(BeautifulSoup(MEGA_HTML, 'lxml'),
                  PAGE_URL.split('/')[-2])

#These both function is for multithreading
def writer(url: str) -> None:
    res: str = mcqscrape_html(url)
    QUIZ_LIST.append(res)

def async_main(url: str) -> None:
    pages: List[str] = [ v for _ , v in pagescrape(url).items()]
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        #This will run writer function in multithread with each quiz url
        executor.map(writer , pages)

    MEGA_HTML = "".join(QUIZ_LIST)
    write_to_html(BeautifulSoup(MEGA_HTML, 'lxml'),
                  PAGE_URL.split('/')[-2])



if __name__ == "__main__":
    command = "Enter the URL of the Page where you see links of all Subject related MCQs: "
    PAGE_URL = args.url or input(command)

    if args.thread:
        async_main(PAGE_URL)
    else:
        main(PAGE_URL)

"""
I did a test run with 10 workers on this link https://www.sanfoundry.com/1000-python-questions-answers/
Normal Function takes around 50 seconds , multithreading takes 17 seconds
"""
        

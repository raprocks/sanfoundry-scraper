import os
import requests
from bs4 import BeautifulSoup
from pprint import pprint

from requests.api import head


def write_to_html(data, filename, group_name):
    if not os.path.exists(group_name):
        os.mkdir(group_name)
    with open(f"./{group_name}/{filename}.html", "w+") as file:
        file.write(str(data))


def mcqscrape_json(url: str):
    # print(title)
    mcqs = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    content = soup.find('div', 'entry-content')
    paras = content.findAll('p')
    header = paras[0].text
    print(header)
    try:
        for each in paras[1:-3]:
            answerid = each.span['id']
            answer_div = content.find('div', id='target-'+answerid)
            # decompose span
            each.span.decompose()
            # print(repr(each.text))
            question = each.text.split("\n")[0].split(".", 1)[-1].strip()
            options = [option.split(')', 1)[-1].strip()
                       for option in each.text.split('\n')[1:] if option != '']
            # print(repr(answer_div.text))
            answer = answer_div.text.split('\n', 1)[0].strip('Answer: ')
            explanation = answer_div.text.split('\n', 1)[1].strip()
            # print(answer)
            question_dict = {
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation
            }
            mcqs.append(question_dict)
    except:
        print("current iteration has ", each)
    return mcqs


def mcqscrape_html(url: str, group_name: str) -> None:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    content = soup.find('div', class_='entry-content')
    heading = soup.find('h1', class_="entry-title").text.split('–')[1].strip()
    print(heading)
    paras = content.findAll('p')
    classes_to_remove = ["sf-mobile-ads",
                         "desktop-content", "mobile-content", "sf-nav-bottom"]
    tags_to_remove = ["script"]
    # remove the answer drop downs
    [sp.decompose() for sp in content.findAll('span', class_="collapseomatic")]
    for class_to_remove in classes_to_remove:
        [sp.decompose() for sp in content.findAll('div', class_=class_to_remove)]
    for tag_to_remove in tags_to_remove:
        [sp.decompose() for sp in content.findAll(tag_to_remove)]
    for tag in paras[-3:]:
        tag.decompose()
    [tag.extract() for tag in content.find_all(
        "div") if tag.text == "advertisement"]
    # span attribute cleanup
    for tag in content.findAll(True):
        tag.attrs.pop("class", "")
        tag.attrs.pop("id", "")
    write_to_html(BeautifulSoup(content.prettify(), 'lxml').prettify(),
                  heading,
                  group_name)


if __name__ == '__main__':
    pprint(mcqscrape_html(
        'https://www.sanfoundry.com/object-oriented-programming-questions-answers-object-reference/'))

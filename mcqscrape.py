import os
import requests
from bs4 import BeautifulSoup


def write_to_html(data, filename):
    if not os.path.exists("Saved_MCQs"):
        os.mkdir("Saved_MCQs")
    with open(f"./Saved_MCQs/{filename}.html", "w+", encoding="utf-8") as file:
        file.write(str(data))


def mcqscrape_json(url: str):
    # print(title)
    mcqs = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html5lib')
    content = soup.find('div', 'entry-content')
    paras = content.findAll('p')
    header = paras[0].text
    print(header)
    each = ''
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
    except Exception as err:
        print("current iteration has ", each)
        print("Error: ", err)
    return mcqs


def mcqscrape_html(url: str) -> str:
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html5lib')
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
        [sp.decompose() for sp in content.findAll('div',
                                                  class_=class_to_remove)]
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
    return content.prettify()
    
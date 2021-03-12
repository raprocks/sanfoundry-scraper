import requests
from bs4 import BeautifulSoup
from pprint import pprint


def mcqscrape(url: str):
    # print(title)
    mcqs = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    content = soup.find('div', 'entry-content')
    paras = content.findAll('p')
    header = paras[0].text
    print(header)
    for each in paras[1:-3]:
        answerid = each.span['id']
        answer_div = content.find('div', id='target-'+answerid)
        # decompose span
        each.span.decompose()
        # print(repr(each.text))
        question = each.text.split("\n")[0].split(".", 1)[-1].strip()
        options = [option.split(')', 1)[-1].strip()
                   for option in each.text.split('\n')[1:] if option != '']
        print(repr(answer_div.text))
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
    return mcqs


if __name__ == '__main__':
    pprint(mcqscrape(
        'https://www.sanfoundry.com/object-oriented-programming-problems/'))

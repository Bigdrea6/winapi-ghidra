import requests as req
from bs4 import BeautifulSoup as bs
import json
import re

from summarize import summarize_sentences

api_summary={}

def make_dict(apis, summaries):
    global api_summary
    if len(apis) != len(summaries):
        print("deduplication is miss")
    else:
        for i in range(len(apis)):
            key = apis[i]
            value = summaries[i]
            api_summary[key] = value

def scrap(soup, n):
    # スクレイピング
    table = soup.find_all('table')

    tds = table[n].find_all('td')
    tds = [(td.get_text()).split(' ', 1) for td in tds]
    print("1. get data")

    # 取得データの整理
    apis = []
    summaries = []
    for td in tds:
        apis.append(td[0])

        td[1] = re.sub("\(.*\)", "", td[1])
        if td[1].count(".") != 1:
            td[1] = summarize_sentences(td[1])
        summaries.append(td[1])
    print("2. make list")

    make_dict(apis, summaries)
    print("3. make dict")

if __name__ == '__main__':
    # いろんな要素の入力
    url = input()
    table_number = int(input())
    f_name = input()

    response = req.get(url)
    soup = bs(response.text, 'html.parser')
    
    scrap(soup, table_number)

    with open(f_name, 'w') as d:
        json.dump(api_summary, d)
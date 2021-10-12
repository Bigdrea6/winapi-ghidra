import re
import requests as req
from bs4 import BeautifulSoup as bs
import json

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

def deduplication(list):
    new_list = []
    for l in list:
        if l not in new_list:
            new_list.append(l)
    
    return new_list

def scrap(soup):
    # スクレイピング
    table = soup.find_all('table')

    tds = table[0].find_all('td')
    tds = [(td.get_text()).split(' ', 1) for td in tds]

    apis = [td[0] for td in tds] 
    summaries = [td[1] for td in tds] 

    for i in range(len(apis)):
        if apis[i][-1] == "A" or apis[i][-1] == "W":
            apis[i] = apis[i][:-1]

    apis = deduplication(apis)
    summaries = deduplication(summaries)

    make_dict(apis, summaries)

    

if __name__ == '__main__':
    with open('summary.json', 'r') as d:
        api_summary = json.load(d)
    
    url = 'https://docs.microsoft.com/en-us/windows/win32/api/winuser/'
    response = req.get(url)
    soup = bs(response.text, 'html.parser')
    
    scrap(soup)

    with open('summary.json', 'w') as d:
        json.dump(api_summary, d)

"""
Error

"""
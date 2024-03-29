import requests
from bs4 import BeautifulSoup
import sqlite3

url_1 = 'https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=1'
url_2 = 'https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=2'
url_3 = 'https://par.cse.nsysu.edu.tw/~advprog/star.php'
html_1 = requests.get(url_1)
html_2 = requests.get(url_2)
html_3 = requests.get(url_3)

sp1 = BeautifulSoup(html_1.text, 'html.parser')
data1 = sp1.select("#col3_content_wrapper")
trs = data1[0].find('table').find_all('tr')
sites = []
key = 0
for tr in trs:
    if key != 0:
        sites.append(tr.find_all('td')[2].find('a')['href'])
    key += 1

sp2 = BeautifulSoup(html_2.text, 'html.parser')
data1 = sp2.select("#col3_content_wrapper")
trs = data1[0].find('table').find_all('tr')
key = 0
for tr in trs:
    if key != 0:
        sites.append(tr.find_all('td')[2].find('a')['href'])
    key += 1

titles = []
for site in sites:
    url = 'https://onlinejudge.org/'+site
    html = requests.get(url)
    data = BeautifulSoup(html.text, 'html.parser')
    data1 = data.select("#col3_content_wrapper")
    trs = data1[0].find('table').find_all('tr')
    key = 0
    for tr in trs:
        if key != 0:
            titles.append(tr.find_all('td')[2].find('a').string)
        key += 1

stars = {}
sp3 = BeautifulSoup(html_3.text, 'html.parser')
data1 = sp3.select("#list0")
trs = data1[0].find_all('tr')
key = 0
for tr in trs:
    if key != 0:
        stars.update(
            {tr.find_all('td')[0].string: tr.find_all('td')[1].string})
    key += 1
conn = sqlite3.connect('Uva.sqlite')
cursor = conn.cursor()

sqlstr = 'CREATE TABLE IF NOT EXISTS uva_topics("id"INTEGER PRIMARY KEY NOT NULL,"serial" INTEGER NOT NULL ,"title" TEXT NOT NULL,"show" TEXT NOT NULL,"topic_url" TEXT NOT NULL,"star" INTEGER)'
cursor.execute(sqlstr)

for title in titles:
    a = title.replace("\xa0", "").split('-', 1)

    if(len(a[0]) == 3):
        substring = 1
    elif(len(a[0]) == 4):
        substring = 2
    else:
        substring = 3
    serial = a[0]

    show = a[0]+" - "+a[1]

    website = "https://onlinejudge.org/external/" + \
        serial[:substring]+"/"+a[0]+".pdf"
    try:
        star = stars[str(a[0])]
    except KeyError:
        star = None
    cursor.execute(
        "insert into uva_topics (serial,title,show,topic_url,star) values (?,?,?,?,?)", (a[0], a[1], show, website, star))

conn.commit()
conn.close()

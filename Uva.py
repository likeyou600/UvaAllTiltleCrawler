import requests
from bs4 import BeautifulSoup
import sqlite3

url_1 = 'https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=1'
url_2 = 'https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=2'
html_1 = requests.get(url_1)
html_2 = requests.get(url_2)

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


conn = sqlite3.connect('Uva.sqlite')
cursor = conn.cursor()

sqlstr = 'CREATE TABLE IF NOT EXISTS codetopic("id"INTEGER PRIMARY KEY NOT NULL,"serial" INTEGER NOT NULL ,"title" TEXT NOT NULL,"topic" TEXT NOT NULL)'
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

    website = "https://onlinejudge.org/external/" + \
        serial[:substring]+"/"+a[0]+".pdf"
    cursor.execute(
        "insert into codetopic (serial,title,topic) values (?,?,?)", (a[0], a[1], website))

conn.commit()
conn.close()

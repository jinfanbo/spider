import requests
from bs4 import BeautifulSoup
import pymysql
import re
import time
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.27 Safari/537.36"
}

url1 = []
def sql(a,b,c,d):
    connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='970320',
        db='前程无忧',
        charset='utf8')
    cursor = connect.cursor()
    cursor.execute('insert into python values(%r,%r,%r,%r)' % (a, b, c, d))
    connect.commit()
    connect.close()
def msg(url):
    title = []
    area = []
    money = []
    req = requests.get(url,headers = headers)
    req.encoding = 'gbk'
    html = req.text
    htmlnem = BeautifulSoup(html,"lxml")
    a = htmlnem.find('div', class_= 'tHeader tHjob')
    a_bf = BeautifulSoup(str(a), "lxml")
    b = a_bf.find('div', class_= 'cn')
    b_bf = BeautifulSoup(str(b), "lxml")
    c = b_bf.find_all('h1')
    for each in c:
        title.append(each.get('title'))
    d = b_bf.find_all('span')
    for each in d:
        area.append(each.string)
    e = b_bf.find_all('strong')
    for each in e:
        money.append(each.string)
        if each.string == None:
            money.insert(0,'空')
    sql(title[0], area[0], money[0], url)
def urllist(url):
    print("爬取："+url)
    req = requests.get(url,headers = headers)
    req.encoding = 'gbk'
    html = req.text
    htmlnem = BeautifulSoup(html, "lxml")
    a = htmlnem.find('div', class_= 'dw_table', id = 'resultList')
    a_bf = BeautifulSoup(str(a), "lxml")
    b = a_bf.find_all('p', class_='t1 ')
    b_bf = BeautifulSoup(str(b), "lxml")
    c = b_bf.find_all('span')
    c_bf = BeautifulSoup(str(c),"lxml")
    d = c_bf.find_all('a')
    for each in d:
        url1.append(each.get('href'))
    for each in url1:
        msg(each)
        time.sleep(10)
    e = a_bf.find_all('li', class_='on')
    page = re.findall('[1-9]\d*', str(e))
    f = a_bf.find_all('span', class_='td')
    allpage = re.findall('[1-9]\d*', str(f))
    if page[0] != allpage[0]:
        g = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,' + str(int(page[0]) + 1) + '.html'
        urllist(g)
urllist('https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html')

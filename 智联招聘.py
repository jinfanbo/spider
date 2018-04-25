import requests
from bs4 import BeautifulSoup
import pymysql
import time

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.27 Safari/537.36'
}

def conmsq(title, url, a, b, c, d, e):
    connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='970320',
        db='智联招聘',
        charset='utf8')
    cursor = connect.cursor()
    cursor.execute("insert into python1 values(%r, %r, %r, %r, %r, %r, %r)" %(title, url, a, b, c, d, e))
    connect.commit()
    connect.close()

def listurl(url):
    req = requests.get(url,headers=headers)
    req.encoding = 'utf-8'
    html = req.text
    html_bf = BeautifulSoup(html, "lxml")
    url1 = html_bf.find_all('td', class_='zwmc')
    url1_bf = BeautifulSoup(str(url1), 'lxml')
    url2 = url1_bf.find_all('a', style='font-weight: bold')
    list1 = [each.get('href') for each in url2 ]
    for each in list1:
        getmsg(each)
        time.sleep(2)
    url3 = html_bf.find_all('li', class_='pagesDown-pos')
    url3_bf = BeautifulSoup(str(url3), 'lxml')
    url4 = url3_bf.find_all('a')
    list2 = [each.get('href') for each in url4]
    if list2[0] != None:
        time.sleep(5)
        listurl(list2[0])

def getmsg(url):
    print("爬取："+url)
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    html = req.text
    html_bf = BeautifulSoup(html, 'lxml')
    url1 = html_bf.find('ul', class_='terminal-ul clearfix')
    url1_bf = BeautifulSoup(str(url1), 'lxml')
    str1 = url1_bf.find_all('strong')
    url2 = html_bf.find('div', class_='inner-left fl')
    url2_bf = BeautifulSoup(str(url2), 'lxml')
    str2 = url2_bf.find_all('h1')
    try:
        title = str2[0].get_text()
        money = str1[0].get_text()
        area = str1[1].get_text()
        exe = str1[4].get_text()
        edu = str1[5].get_text()
        sort = str1[7].get_text()
        conmsq(title, url, money, area, exe, edu, sort)
    except Exception as e:
        pass

listurl('https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=python&p=1&isadv=0')
# 3分钟
import requests
from bs4 import BeautifulSoup
import pymongo
import time
import random
import threading

class MaitianSpider(object):
    def __init__(self):
        self.url = 'http://bj.maitian.cn/esfall/PG'
        self.headers = {
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 67.0.3396.99 Safari / 537.36'
        }
        self.proxies = [
            '183.62.196.10:3128',
            '125.62.26.197:3128',
            '218.60.8.83:3129',
            '221.7.255.168:8080',
            '218.60.8.99:3129',
            '61.135.217.7:80',
            '180.168.13.26:8000',
            '106.75.225.83:808'
        ]
        self.data = []

    def GetHtmlTxt(self, url):
        retry_count = 11
        while retry_count > 0:
            try:
                ip = random.choice(self.proxies)
                print(ip)
                response = requests.get(url, headers = self.headers, proxies = {'http':ip}, timeout = 1)
                htmltxt = response.content.decode('utf-8')
                return htmltxt
            except Exception as e:
                print('GetHtmlTxt错误:' + str(e))
                retry_count -= 1
        return None

    def ParseGetData(self, htmltxt):
        bs_html = BeautifulSoup(htmltxt, 'lxml')
        room_list = bs_html.select('.list_title')
        for room in room_list:
            room_dict = {}
            room_dict['title'] = room.select_one('h1 a').get_text()
            room_dict['url'] = 'http://bj.maitian.cn' + room.select_one('h1 a').get('href')
            room_dict['info'] = room.select_one('p').get_text().replace('\r','').replace('\n','').replace(' ','').replace('\xa0','')
            room_dict['price'] = room.select_one('.the_price').get_text().replace('\n','')
            room_dict['others'] = room.select_one('.morel.clearfix').get_text().replace('\n','')
            self.data.append(room_dict)

    def DataSave(self):
        mongo = pymongo.MongoClient()
        collection = mongo.maitian1.room
        collection.insert(self.data)
        mongo.close()

    def StarSpider(self, page):
        url = self.url + str(page)
        print('爬取:' + url)
        htmltxt = self.GetHtmlTxt(url)
        try:
            self.ParseGetData(htmltxt)
        except Exception as e:
            print('ParseGetData错误：' + str(e))

if __name__ == '__main__':
    spider1 = MaitianSpider()
    for i in range(1,999):
        spider1.StarSpider(i)
    spider1.DataSave()
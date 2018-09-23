import requests
from bs4 import BeautifulSoup
import pymongo
import time
import random

class MaitianSpider(object):
    def __init__(self):
        self.url = 'http://bj.maitian.cn/esfall/PG'
        self.headers = {
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 67.0.3396.99 Safari / 537.36'
        }
        self.proxies = {
            'http':'http://183.62.196.10:3128',
        }
        self.data = []

    def GetHtmlTxt(self, url):
        try:
            response = requests.get(url, headers = self.headers, proxies = self.proxies)
            htmltxt = response.content.decode('utf-8')
        except Exception as e:
            print('GetHtmlTxt错误:' + str(e))
        else:
            return htmltxt

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
        collection = mongo.maitian.room
        collection.insert(self.data)
        mongo.close()

    def StarSpider(self):
        for i in range(1,999):
            url = self.url + str(i)
            print('爬取:' + url)
            spidertime = random.randint(1,10)
            htmltxt = self.GetHtmlTxt(url)
            try:
                self.ParseGetData(htmltxt)
                time.sleep(spidertime)
            except Exception as e:
                print('ParseGetData错误：' + str(e))
        self.DataSave()

if __name__ == '__main__':
    spider1 = MaitianSpider()
    spider1.StarSpider()